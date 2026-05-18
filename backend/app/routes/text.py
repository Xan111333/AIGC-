from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.text_service import create_text_generation, get_generation_records, get_generation_record
from ..schemas.generation import TextGenerationRequest, GenerationRecordResponse
from ..utils.depends import get_current_active_user
from ..models import User

router = APIRouter(prefix="/api/text", tags=["文本生成"])

@router.post("/generate", response_model=GenerationRecordResponse)
def generate_text(
    request: TextGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="提示词不能为空")
    
    record = create_text_generation(db, current_user.id, request)
    return record

@router.get("/history", response_model=list[GenerationRecordResponse])
def get_text_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_generation_records(db, current_user.id, "text", skip, limit)

@router.get("/history/{record_id}", response_model=GenerationRecordResponse)
def get_text_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = get_generation_record(db, record_id, current_user.id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    return record