from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.audio_service import create_audio_generation, get_generation_records, get_generation_record
from ..schemas.generation import AudioGenerationRequest, GenerationRecordResponse
from ..utils.depends import get_current_active_user
from ..models import User
from ..services.edge_tts_service import get_supported_voices

router = APIRouter(prefix="/api/audio", tags=["音频生成"])

@router.get("/voices")
def get_voices():
    return {"voices": get_supported_voices()}

@router.post("/generate", response_model=GenerationRecordResponse)
def generate_audio(
    request: AudioGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文本内容不能为空")
    
    if len(request.text) > 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="文本内容不能超过1024字符")
    
    if request.speed < 0 or request.speed > 15:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="语速参数必须在 0-15 之间")
    
    if request.pitch < 0 or request.pitch > 15:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="音调参数必须在 0-15 之间")
    
    try:
        record = create_audio_generation(db, current_user.id, request)
        return record
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/history", response_model=list[GenerationRecordResponse])
def get_audio_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return get_generation_records(db, current_user.id, "audio", skip, limit)

@router.get("/history/{record_id}", response_model=GenerationRecordResponse)
def get_audio_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = get_generation_record(db, record_id, current_user.id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    return record
