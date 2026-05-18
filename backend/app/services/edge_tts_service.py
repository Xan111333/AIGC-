import edge_tts
import uuid
import asyncio
from pathlib import Path
from ..utils.local_storage import storage_root, settings

SUPPORTED_VOICES = {
    "zh-CN-XiaoxiaoNeural": "晓晓（女声，默认）",
    "zh-CN-XiaoyiNeural": "晓伊（女声，活泼）",
    "zh-CN-YunxiNeural": "云希（男声）",
    "zh-CN-YunyangNeural": "云扬（男声，新闻）",
    "zh-CN-liaoning-XiaobeiNeural": "小北（东北话女声）"
}

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
DEFAULT_RATE = "+0%"
DEFAULT_PITCH = "+0Hz"

def _get_speed_to_rate(speed: float) -> str:
    if speed <= 5:
        return f"-{int((5 - speed) * 10)}%"
    elif speed == 7.5:
        return "+0%"
    else:
        return f"+{int((speed - 7.5) * 4)}%"

def _get_pitch_to_edge_pitch(pitch: float) -> str:
    if pitch <= 5:
        return f"-{int((5 - pitch) * 10)}Hz"
    elif pitch == 7.5:
        return "+0Hz"
    else:
        return f"+{int((pitch - 7.5) * 4)}Hz"

async def generate_audio_with_edge_tts(
    text: str,
    voice: str = DEFAULT_VOICE,
    speed: float = 7.5,
    pitch: float = 7.5
) -> str:
    voice_name = voice if voice in SUPPORTED_VOICES else DEFAULT_VOICE
    rate = _get_speed_to_rate(speed)
    edge_pitch = _get_pitch_to_edge_pitch(pitch)

    audio_dir = storage_root / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    filename = f"audio_{uuid.uuid4().hex}.mp3"
    filepath = audio_dir / filename

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice_name,
        rate=rate,
        pitch=edge_pitch
    )
    await communicate.save(str(filepath))

    return f"{settings.STORAGE_URL_PREFIX}/audio/{filename}"

def generate_audio_sync(
    text: str,
    voice: str = DEFAULT_VOICE,
    speed: float = 7.5,
    pitch: float = 7.5
) -> str:
    return asyncio.run(generate_audio_with_edge_tts(text, voice, speed, pitch))

def get_supported_voices() -> dict:
    return SUPPORTED_VOICES
