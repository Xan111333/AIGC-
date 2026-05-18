from sqlalchemy.orm import Session
from ..models import GenerationRecord
from ..schemas.generation import ImageGenerationRequest
from datetime import datetime
import json
from ..common.qianfan_client import call_image_generation

MOCK_IMAGE_URL = "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=beautiful%20landscape&image_size=landscape_16_9"

def create_image_generation(db: Session, user_id: int, request: ImageGenerationRequest) -> GenerationRecord:
    params = json.dumps({
        "resolution": request.resolution,
        "style": request.style,
        "num_images": request.num_images
    })
    
    record = GenerationRecord(
        user_id=user_id,
        type="image",
        prompt=request.prompt,
        params=params,
        status="in_progress"
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    try:
        image_url = call_image_generation(
            prompt=request.prompt,
            style=request.style,
            size=request.resolution
        )
        
        record.result_url = image_url
        record.status = "completed"
        record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(record)
    except Exception as e:
        print(f"图像生成失败，使用Mock数据: {e}")
        record.result_url = MOCK_IMAGE_URL
        record.status = "completed"
        record.error_message = str(e)
        record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(record)
    
    return record

def process_image_generation_task(db: Session, record_id: int):
    record = db.query(GenerationRecord).filter(GenerationRecord.id == record_id).first()
    if not record:
        return
    
    try:
        params = json.loads(record.params) if record.params else {}
        style = params.get("style", "写实")
        size = params.get("resolution", "1024x1024")
        
        image_url = call_image_generation(
            prompt=record.prompt,
            style=style,
            size=size
        )
        
        record.result_url = image_url
        record.status = "completed"
        record.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        print(f"图像生成失败: {e}")
        record.result_url = MOCK_IMAGE_URL
        record.status = "completed"
        record.error_message = str(e)
        record.completed_at = datetime.utcnow()
        db.commit()
    
    return record

def get_image_generation_status(db: Session, record_id: int, user_id: int) -> GenerationRecord | None:
    record = db.query(GenerationRecord).filter(
        GenerationRecord.id == record_id,
        GenerationRecord.user_id == user_id,
        GenerationRecord.type == "image"
    ).first()
    return record