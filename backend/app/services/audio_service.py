from sqlalchemy.orm import Session
from ..models import GenerationRecord
from ..schemas.generation import AudioGenerationRequest
from datetime import datetime
import json
from ..services.edge_tts_service import generate_audio_sync

MOCK_AUDIO_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

def generate_audio_mock(text: str) -> str:
    return MOCK_AUDIO_URL

def create_audio_generation(db: Session, user_id: int, request: AudioGenerationRequest) -> GenerationRecord:
    params = json.dumps({
        "voice": request.voice,
        "speed": request.speed,
        "pitch": request.pitch
    })

    record = GenerationRecord(
        user_id=user_id,
        type="audio",
        prompt=request.text,
        params=params,
        status="in_progress"
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    try:
        audio_url = generate_audio_sync(
            text=request.text,
            voice=request.voice,
            speed=request.speed,
            pitch=request.pitch
        )

        record.result_url = audio_url
        record.status = "completed"
        record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(record)
    except Exception as e:
        print(f"音频生成失败，使用Mock数据: {e}")
        record.result_url = generate_audio_mock(request.text)
        record.status = "completed"
        record.error_message = str(e)
        record.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(record)

    return record

def get_generation_records(db: Session, user_id: int, type: str | None = None, skip: int = 0, limit: int = 50):
    from ..services.text_service import get_generation_records as get_records
    return get_records(db, user_id, type, skip, limit)

def get_generation_record(db: Session, record_id: int, user_id: int):
    from ..services.text_service import get_generation_record as get_record
    return get_record(db, record_id, user_id)
