import requests
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('ZHIPU_API_KEY', '')

print("=== 测试智谱 AI 音频生成 API ===")
print(f"API Key: {api_key[:20]}...")

url = "https://open.bigmodel.cn/api/paas/v4/audio/speech"

payload = {
    "model": "glm-tts",
    "input": "你好，欢迎使用智谱AI语音合成功能。这是一段测试音频。",
    "voice": "female",
    "speed": 1.0,
    "volume": 1.0,
    "response_format": "wav"
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {api_key}"
}

print()
print(f"Model: glm-tts")
print(f"Voice: female")
print(f"Text: 你好，欢迎使用智谱AI语音合成功能...")
print()

response = requests.post(url, headers=headers, json=payload, timeout=120)

print(f"状态码: {response.status_code}")

content_type = response.headers.get("Content-Type", "")
print(f"Content-Type: {content_type}")

if "audio" in content_type or "wav" in content_type:
    print()
    print("[OK] 音频生成成功！")
    print(f"音频大小: {len(response.content)} bytes")

    output_file = "test_audio.wav"
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"音频已保存到: {output_file}")
else:
    print(f"响应文本: {response.text[:800]}")
