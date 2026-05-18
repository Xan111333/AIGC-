from sqlalchemy.orm import Session
from ..models import GenerationRecord
from ..schemas.generation import TextGenerationRequest
from datetime import datetime
import json
from ..services.zhipu_service import generate_text_with_zhipu

def create_text_generation(db: Session, user_id: int, request: TextGenerationRequest) -> GenerationRecord:
    params = json.dumps({
        "length": request.length,
        "style": request.style,
        "tone": request.tone,
        "language": request.language
    })

    record = GenerationRecord(
        user_id=user_id,
        type="text",
        prompt=request.prompt,
        params=params,
        status="in_progress"
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    try:
        text_result = generate_text_with_zhipu(
            prompt=request.prompt,
            style=request.style,
            length=request.length,
            tone=request.tone
        )

        record.result_url = text_result
        record.status = "completed"
        record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(record)
    except Exception as e:
        print(f"文本生成失败: {e}")
        record.result_url = f"生成失败: {str(e)}"
        record.status = "completed"
        record.error_message = str(e)
        record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(record)

    return record

def get_generation_records(db: Session, user_id: int, type: str | None = None, skip: int = 0, limit: int = 50):
    query = db.query(GenerationRecord).filter(GenerationRecord.user_id == user_id)
    if type:
        query = query.filter(GenerationRecord.type == type)
    return query.order_by(GenerationRecord.created_at.desc()).offset(skip).limit(limit).all()

def get_generation_record(db: Session, record_id: int, user_id: int):
    record = db.query(GenerationRecord).filter(
        GenerationRecord.id == record_id,
        GenerationRecord.user_id == user_id
    ).first()
    return record
