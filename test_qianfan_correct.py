import requests

ak_new = "ALTAKJIQMn6vMxXxWEjExJBHq"
sk_new = "36772a58ee9d49ac92d0cc7cd345a692"

print("="*60)
print("测试正确的调用方式")
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
            
            print("\n" + "="*60)
            print("测试文生图API")
            print("="*60)
            
            api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/text2image/sd_xl?access_token={access_token}"
            
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/json"},
                json={
                    "prompt": "一只可爱的小猫，写实风格",
                    "width": 512,
                    "height": 512,
                    "steps": 20,
                    "n": 1
                },
                timeout=120
            )
            
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {result}")
            
        else:
            print(f"\n❌ 未获取到Token: {result}")
            
except Exception as e:
    print(f"错误: {e}")
