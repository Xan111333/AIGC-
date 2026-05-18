import os
import sys
import requests
from dotenv import load_dotenv
load_dotenv()

ak = os.getenv('QIANFAN_AK', '')
sk = os.getenv('QIANFAN_SK', '')

print("=== 测试多种 API 方式 ===\n")
print(f"AK: {ak[:20]}...")
print(f"SK: {sk[:20]}...")
print()

print("=== 方式1: 获取 IAM access_token (OAuth2) ===")
token_url = "https://aip.baidubce.com/oauth/2.0/token"
params = {
    "grant_type": "client_credentials",
    "client_id": ak,
    "client_secret": sk
}
resp = requests.get(token_url, params=params, timeout=30)
result = resp.json()
print(f"状态码: {resp.status_code}")
print(f"响应: {str(result)[:200]}")

if 'access_token' in result:
    token = result['access_token']
    print(f"[OK] token: {token[:30]}...")
    
    print()
    print("=== 方式1a: 文心工作室 API (sd_xl) ===")
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token={token}"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": "a beautiful sunset",
        "negative_prompt": "",
        "size": "1024x1024",
        "steps": 20,
        "n": 1,
        "sampler_index": "DPM++ SDE Karras"
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=120)
        result = resp.json()
        print(f"状态码: {resp.status_code}")
        print(f"响应: {str(result)[:300]}")
    except Exception as e:
        print(f"错误: {e}")
else:
    print("[FAIL] 无法获取 token，跳过方式1a")

print()
print("=== 方式2: 千帆 v2 API (URL参数传 AK/SK) ===")
try:
    url = f"https://qianfan.baidubce.com/v2/images/generations?ak={ak}&sk={sk}"
    headers = {"Content-Type": "application/json"}
    data = {"model": "irag-1.0", "prompt": "a beautiful sunset"}
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    result = resp.json()
    print(f"状态码: {resp.status_code}")
    print(f"响应: {str(result)[:300]}")
except Exception as e:
    print(f"错误: {e}")

print()
print("=== 方式3: ERNIE iRAG API (Bearer token) ===")
try:
    bearer = f"bce-v3/{ak}/{sk}"
    url = "https://qianfan.baidubce.com/v2/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer}"
    }
    data = {"model": "irag-1.0", "prompt": "a beautiful sunset"}
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    result = resp.json()
    print(f"状态码: {resp.status_code}")
    print(f"响应: {str(result)[:300]}")
except Exception as e:
    print(f"错误: {e}")

print()
print("=== 测试完成 ===")
