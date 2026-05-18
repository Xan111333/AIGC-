import requests

ak_from_screenshot = "YOUR_BAIDU_AK"
sk_current = "YOUR_BAIDU_SK"

print("="*60)
print("测试截图中的AK + 当前SK")
print("="*60)
print(f"AK: {ak_from_screenshot}")
print(f"SK: {sk_current}")

try:
    token_url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak_from_screenshot}&client_secret={sk_current}"
    response = requests.post(token_url, timeout=30)
    
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
except Exception as e:
    print(f"错误: {e}")
