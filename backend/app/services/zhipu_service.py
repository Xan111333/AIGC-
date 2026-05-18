import requests
import json
from ..utils.api_config import APIConfig

MOCK_TEXT_RESPONSES = {
    "story": [
        "在一个遥远的星球上，住着一群善良的外星人。他们用音乐来交流，用星光来照明。每天晚上，他们都会举办盛大的音乐会...",
        "从前有一只会说话的小猫，它的梦想是成为一名画家。它用爪子握着画笔，在画布上画出了五彩斑斓的世界...",
        "深海里有一座神秘的城堡，里面住着美人鱼公主。她的歌声能让暴风雨平息，能让鱼儿们翩翩起舞..."
    ],
    "poem": [
        "月光如水洒窗前，\n思绪万千夜难眠。\n遥望星河遥无际，\n梦里寻你到天边。",
        "春风拂面柳丝摇，\n细雨绵绵润麦苗。\n鸟语花香人欲醉，\n江山如画分外娇。"
    ],
    "article": [
        "人工智能正在改变我们的生活方式。从智能家居到自动驾驶，AI技术已经渗透到我们生活的方方面面...",
        "阅读是一种享受，它能开阔我们的视野，丰富我们的知识。一本好书就像一位良师益友..."
    ],
    "neutral": [
        "根据您的需求，我为您生成了以下内容。希望能够满足您的期望...",
        "这是根据您提供的提示生成的文本..."
    ]
}

def generate_text_with_zhipu(prompt: str, style: str = "neutral", length: str = "medium", tone: str = "neutral") -> str:
    if not APIConfig.has_zhipu_key():
        return generate_text_mock(prompt, style)

    try:
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {APIConfig.ZHIPU_API_KEY}",
            "Content-Type": "application/json"
        }

        system_prompt = get_system_prompt(style, length, tone)

        data = {
            "model": "glm-4-flash",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": get_max_tokens(length)
        }

        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"智谱 AI API 错误: {e}")
        return generate_text_mock(prompt, style)

def get_system_prompt(style: str, length: str, tone: str) -> str:
    style_map = {
        "story": "你是一位专业的故事作家，请创作一个引人入胜的故事。",
        "poem": "你是一位诗人，请创作一首优美的诗歌。",
        "article": "你是一位专业撰稿人，请撰写一篇有深度的文章。",
        "neutral": "你是一位AI助手，请根据用户的需求提供帮助。",
        "creative": "你是一位创意写作大师，请发挥想象力进行创作。",
        "academic": "你是一位学者，请撰写学术风格的内容。"
    }

    length_map = {
        "short": "请保持回答简洁，控制在100字以内。",
        "medium": "请提供中等长度的回答，约200-300字。",
        "long": "请提供详细的回答，约500字左右。"
    }

    tone_map = {
        "neutral": "语气保持中立客观。",
        "friendly": "语气友好亲切。",
        "professional": "语气专业正式。",
        "humorous": "语气幽默风趣。",
        "enthusiastic": "语气热情洋溢。"
    }

    style_prompt = style_map.get(style, style_map["neutral"])
    length_prompt = length_map.get(length, length_map["medium"])
    tone_prompt = tone_map.get(tone, tone_map["neutral"])

    return f"{style_prompt} {length_prompt} {tone_prompt}"

def get_max_tokens(length: str) -> int:
    length_map = {
        "short": 150,
        "medium": 400,
        "long": 800
    }
    return length_map.get(length, 400)

def generate_text_mock(prompt: str, style: str) -> str:
    import random
    category = style.lower()
    if category not in MOCK_TEXT_RESPONSES:
        category = "neutral"
    return random.choice(MOCK_TEXT_RESPONSES[category])
