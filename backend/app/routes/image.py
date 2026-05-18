from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.image_service import create_image_generation, process_image_generation_task, get_image_generation_status
from ..schemas.generation import ImageGenerationRequest, GenerationRecordResponse
from ..utils.depends import get_current_active_user
from ..models import User
from ..services.text_service import get_generation_records, get_generation_record

router = APIRouter(prefix="/api/image", tags=["图像生成"])

@router.post("/generate", response_model=GenerationRecordResponse)
def generate_image(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="提示词不能为空")
    
    record = create_image_generation(db, current_user.id, request)
    
    background_tasks.add_task(process_image_generation_task, db, record.id)
    
    return record

@router.get("/status/{task_id}", response_model=GenerationRecordResponse)
def get_generation_status(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = get_image_generation_status(db, task_id, current_user.id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
    return record

@router.get("/history", response_model=list[GenerationRecordResponse])
def get_image_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_generation_records(db, current_user.id, "image", skip, limit)

@router.get("/history/{record_id}", response_model=GenerationRecordResponse)
def get_image_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = get_generation_record(db, record_id, current_user.id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    return record