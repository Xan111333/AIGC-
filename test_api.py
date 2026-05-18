import requests
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

print("="*60)
print("测试 DeepSeek API")
print("="*60)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

print(f"API Key: {DEEPSEEK_API_KEY[:20]}...")

try:
    response = requests.post(
        DEEPSEEK_API_URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个帮助助手"},
                {"role": "user", "content": "你好，请用一句话回复"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        },
        timeout=30
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text[:500]}")
    
except Exception as e:
    print(f"错误: {e}")

print("\n" + "="*60)
print("测试 百度千帆 API")
print("="*60)

QIANFAN_AK = os.getenv("QIANFAN_AK", "")
QIANFAN_SK = os.getenv("QIANFAN_SK", "")

print(f"AK: {QIANFAN_AK[:10]}...")
print(f"SK: {QIANFAN_SK[:10]}...")

try:
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={QIANFAN_AK}&client_secret={QIANFAN_SK}"
    response = requests.post(token_url, timeout=30)
    
    print(f"Token 状态码: {response.status_code}")
    print(f"Token 响应: {response.text[:500]}")
    
    if response.status_code == 200:
        result = response.json()
        access_token = result.get("access_token")
        if access_token:
            print(f"\n获取到Token: {access_token[:20]}...")
        else:
            print(f"\n未获取到Token: {result}")
            
except Exception as e:
    print(f"错误: {e}")
