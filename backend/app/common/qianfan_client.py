import requests
import os
import time
import base64
from datetime import datetime
import uuid
from ..utils.api_config import APIConfig


def call_image_generation(
    prompt: str,
    style: str = "写实",
    size: str = "1024x1024",
) -> str:
    """
    调用智谱 AI 图像生成 API (CogView-4
    """
    if not prompt or not prompt.strip():
        raise ValueError("提示词不能为空")

    if not APIConfig.has_zhipu_key():
        raise ValueError("智谱 AI API 密钥未配置")

    api_key = APIConfig.ZHIPU_API_KEY

    style_prompt = _get_style_prompt(style)
    full_prompt = f"{prompt}, {style_prompt}"

    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "cogview-4",
        "prompt": full_prompt,
        "size": size
    }

    print(f"调用智谱 CogView-4 图像生成...")
    print(f"提示词: {full_prompt}")

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)

        if response.status_code != 200:
            error_text = response.text[:500]
            raise ValueError(f"API 返回错误: {response.status_code} - {error_text}")

        result = response.json()

        if "error" in result:
            raise ValueError(f"API 返回错误: {result}")

        if "data" in result and len(result["data"]) > 0:
            img_url = result["data"][0].get("url")
            if img_url:
                return img_url
            img_b64 = result["data"][0].get("b64_json")
            if img_b64:
                return _save_base64_image(img_b64)

        raise ValueError(f"响应格式错误: {str(result)[:200]}")

    except requests.RequestException as e:
        raise ValueError(f"网络请求失败: {e}")


def call_text_to_speech(
    text: str,
    speed: int = 5,
    pitch: int = 5,
    voice: str = "彤彤",
) -> str:
    """
    调用智谱 AI 语音合成 API (GLM-TTS
    """
    if not text or not text.strip():
        raise ValueError("文本不能为空")

    if len(text) > 4096:
        raise ValueError("文本长度不能超过 4096 字符")

    if not APIConfig.has_zhipu_key():
        raise ValueError("智谱 AI API 密钥未配置")

    api_key = APIConfig.ZHIPU_API_KEY

    url = "https://open.bigmodel.cn/api/paas/v4/audio/speech"

    speed_value = _get_speed_value(speed)
    voice_value = _get_voice_value(voice)

    data = {
        "model": "glm-tts",
        "input": text,
        "voice": voice_value,
        "speed": speed_value,
        "response_format": "mp3"
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"调用智谱 GLM-TTS 语音合成...")
    print(f"文本: {text[:50]}...")
    print(f"音色: {voice_value}")

    try:
        response = requests.post(url, headers=headers, json=data, timeout=120)

        if response.status_code != 200:
            error_text = response.text[:500]
            raise ValueError(f"API 返回错误: {response.status_code} - {error_text}")

        content_type = response.headers.get("Content-Type", "")
        if "audio" in content_type or "mp3" in content_type:
            return _save_audio_data(response.content)

        raise ValueError("语音合成失败，未返回有效音频数据")

    except requests.RequestException as e:
        raise ValueError(f"网络请求失败: {e}")


def _get_style_prompt(style: str) -> str:
    style_map = {
        "写实": "写实风格，高清晰度，真实感强",
        "写实风格": "写实风格，高清晰度，真实感强",
        "realistic": "写实风格，高清晰度，真实感强",
        "卡通": "卡通风格，可爱的动画效果，色彩鲜艳",
        "卡通风格": "卡通风格，可爱的动画效果，色彩鲜艳",
        "cartoon": "卡通风格，可爱的动画效果，色彩鲜艳",
        "油画": "油画风格，艺术感强，笔触丰富",
        "油画风格": "油画风格，艺术感强，笔触丰富",
        "oil": "油画风格，艺术感强，笔触丰富",
        "oil-painting": "油画风格，艺术感强，笔触丰富",
        "水彩": "水彩风格，柔和清新，色彩淡雅",
        "水彩风格": "水彩风格，柔和清新，色彩淡雅",
        "watercolor": "水彩风格，柔和清新，色彩淡雅",
        "动漫": "动漫风格，日式动画效果",
        "anime": "动漫风格，日式动画效果",
        "科幻": "科幻风格，未来感十足",
        "sci-fi": "科幻风格，未来感十足",
        "像素风": "像素风格，复古游戏感",
        "pixel": "像素风格，复古游戏感",
        "赛博朋克": "赛博朋克风格，霓虹灯效果，未来都市",
        "cyberpunk": "赛博朋克风格，霓虹灯效果，未来都市",
        "复古": "复古风格，怀旧感，经典配色",
        "vintage": "复古风格，怀旧感，经典配色",
    }
    return style_map.get(style, style_map["写实"])


def _get_voice_value(voice: str) -> str:
    voice_map = {
        "彤彤": "female",
        "女": "female",
        "女声": "female",
        "female": "female",
        "小陈": "male",
        "男": "male",
        "男声": "male",
        "male": "male",
        "锤锤": "chuichui",
        "jam": "jam",
        "kazi": "kazi",
        "douji": "douji",
        "luodo": "luodo",
    }
    return voice_map.get(voice, "female")


def _get_speed_value(speed: int) -> float:
    speed_value = 0.5 + (speed / 5)
    return max(0.5, min(2.0, speed_value))


def _save_base64_image(b64_data: str) -> str:
    """
    将 base64 图片保存并返回 URL
    """
    from ..utils.local_storage import upload_bytes

    try:
        image_data = base64.b64decode(b64_data)
        filename = f"generated/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.png"

        url = upload_bytes(image_data, filename, "image/png")
        print(f"图片已保存: {filename}")
        return url
    except Exception as e:
        print(f"保存图片失败: {e}")
        return f"data:image/png;base64,{b64_data}"


def _save_audio_data(audio_data: bytes) -> str:
    """
    保存音频数据并返回 URL
    """
    from ..utils.local_storage import upload_bytes

    try:
        filename = f"generated/audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.mp3"

        url = upload_bytes(audio_data, filename, "audio/mpeg")
        print(f"音频已保存: {filename}")
        return url
    except Exception as e:
        print(f"保存音频失败: {e}")
        b64_audio = base64.b64encode(audio_data).decode('utf-8')
        return f"data:audio/mp3;base64,{b64_audio}"
