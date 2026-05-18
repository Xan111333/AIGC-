import os
import requests
from dotenv import load_dotenv
load_dotenv()

ak = os.getenv('QIANFAN_AK', '')
sk = os.getenv('QIANFAN_SK', '')

print("=== 测试百度千帆图像生成 API ===")
print(f"AK: {ak[:20]}...")
print(f"SK: {sk[:20]}...")

print()
print("1. 测试获取 access token...")
try:
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": ak,
        "client_secret": sk
    }
    resp = requests.get(url, params=params, timeout=30)
    result = resp.json()
    
    if 'access_token' in result:
        access_token = result['access_token']
        print(f"   OK: token = {access_token[:30]}...")
    else:
        print(f"   失败: {result}")
        exit(1)
except Exception as e:
    print(f"   错误: {e}")
    exit(1)

print()
print("2. 测试 Stable-Diffusion-XL 图像生成...")
try:
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token={access_token}"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": "a beautiful sunset",
        "negative_prompt": "",
        "size": "1024x1024",
        "steps": 20,
        "n": 1,
        "sampler_index": "DPM++ SDE Karras"
    }
    resp = requests.post(url, headers=headers, json=data, timeout=120)
    result = resp.json()
    
    print(f"   状态码: {resp.status_code}")
    print(f"   响应: {str(result)[:300]}")
    
    if 'error_code' in result:
        print(f"   失败: {result.get('error_msg', '未知错误')}")
    elif 'data' in result:
        print(f"   OK: 生成了 {len(result['data'])} 张图片")
except Exception as e:
    print(f"   错误: {e}")

print()
print("=== 测试完成 ===")
