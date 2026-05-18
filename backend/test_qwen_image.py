import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

ak = os.getenv('QIANFAN_AK', '')
sk = os.getenv('QIANFAN_SK', '')

print("=== 测试 qwen-image 模型 ===")
print(f"AK: {ak[:20]}...")
print(f"SK: {sk[:20]}...")

url = "https://qianfan.baidubce.com/v2/images/generations"
bearer = f"bce-v3/{ak}/{sk}"

payload = {
    "model": "qwen-image",
    "prompt": "画一只小狗"
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {bearer}"
}

print()
print(f"Authorization: Bearer bce-v3/{ak[:10]}.../{sk[:8]}...")
print(f"Model: qwen-image")
print()

data = json.dumps(payload)

response = requests.post(url, headers=headers, data=data, timeout=60)

print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

result = response.json()
if 'data' in result and len(result['data']) > 0:
    print()
    print("[OK] 生成成功！")
    print(f"图片URL: {result['data'][0].get('url', 'N/A')}")
