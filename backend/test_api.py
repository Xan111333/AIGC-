import os
import sys
from dotenv import load_dotenv
load_dotenv()

print("=== 测试百度千帆 API ===")
ak = os.getenv('QIANFAN_AK', '')
sk = os.getenv('QIANFAN_SK', '')
print(f"AK: {ak[:20]}...")
print(f"SK: {sk[:20]}...")

print()
print("方法 1: 测试百度智能云 AI 开放平台 API...")
try:
    import requests
    
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": ak,
        "client_secret": sk
    }
    resp = requests.get(url, params=params, timeout=30)
    result = resp.json()
    if 'access_token' in result:
        print(f"[OK] 百度智能云 AI 开放平台 API 可用")
        print(f"     token: {result['access_token'][:30]}...")
    else:
        print(f"[FAIL] {result}")
except Exception as e:
    print(f"[ERROR] {e}")

print()
print("方法 2: 测试百度千帆大模型平台 SDK...")
try:
    import qianfan
    qianfan.AK = ak
    qianfan.SK = sk
    
    chat_comp = qianfan.ChatCompletion()
    resp = chat_comp.do(model="ERNIE-Lite-8K", messages=[
        {"role": "user", "content": "你好"}
    ])
    print(f"[OK] 千帆 SDK 可用")
    print(f"     响应: {str(resp.get('body', {})).get('result', 'OK') if isinstance(resp, dict) else 'OK'}"[:100])
except ImportError:
    print("[SKIP] qianfan SDK 未安装")
except Exception as e:
    print(f"[FAIL] {e}")

print()
print("方法 3: 测试百度千帆大模型平台直接 API...")
try:
    import requests
    
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token={ak}"
    headers = {"Content-Type": "application/json"}
    data = {"messages": [{"role": "user", "content": "你好"}]}
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    result = resp.json()
    if 'error_code' in result:
        print(f"[FAIL] {result}")
    else:
        print(f"[OK] 千帆直接 API 可用")
        print(f"     响应: {str(result)[:100]}")
except Exception as e:
    print(f"[ERROR] {e}")

print()
print("=== 测试完成 ===")
