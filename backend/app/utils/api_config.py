import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    # 智谱 AI 配置
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")

    ZHIPU_CHAT_URL = os.getenv(
        "ZHIPU_CHAT_URL",
        "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    )
    ZHIPU_IMAGE_URL = os.getenv(
        "ZHIPU_IMAGE_URL",
        "https://open.bigmodel.cn/api/paas/v4/images/generations"
    )
    ZHIPU_TTS_URL = os.getenv(
        "ZHIPU_TTS_URL",
        "https://open.bigmodel.cn/api/paas/v4/audio/speech"
    )

    @classmethod
    def has_zhipu_key(cls):
        return bool(cls.ZHIPU_API_KEY)
