import requests

ak_new = "YOUR_BCE_AK"
sk_new = "YOUR_BAIDU_SK"

print("="*60)
print("测试最新的密钥")
print("="*60)
print(f"AK: {ak_new}")
print(f"SK: {sk_new}")

try:
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": ak_new,
        "client_secret": sk_new
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        access_token = result.get("access_token")
        if access_token:
            print(f"\n✅ 获取到Token: {access_token[:30]}...")
        else:
            print(f"\n❌ 未获取到Token: {result}")
            
except Exception as e:
    print(f"错误: {e}")
