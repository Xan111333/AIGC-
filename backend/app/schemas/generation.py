from pydantic import BaseModel
from datetime import datetime

class TextGenerationRequest(BaseModel):
    prompt: str
    length: str = "medium"
    style: str = "neutral"
    tone: str = "neutral"
    language: str = "zh"

class ImageGenerationRequest(BaseModel):
    prompt: str
    resolution: str = "1024x1024"
    style: str = "realistic"
    num_images: int = 1

class VideoGenerationRequest(BaseModel):
    prompt: str
    duration: int = 5
    resolution: str = "720p"
    style: str = "realistic"

class AudioGenerationRequest(BaseModel):
    text: str
    voice: str = "女"
    speed: int = 5
    pitch: int = 5

class GenerationResponse(BaseModel):
    id: int
    type: str
    prompt: str
    result: str
    status: str
    created_at: datetime
    completed_at: datetime | None = None

class GenerationRecordResponse(BaseModel):
    id: int
    type: str
    prompt: str
    params: str | None
    result_url: str | None
    status: str
    created_at: datetime
    completed_at: datetime | None = None