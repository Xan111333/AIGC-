import os
import requests
from dotenv import load_dotenv
load_dotenv()

print('=== 百度智能云 API 配置检查 ===')
ak = os.getenv('QIANFAN_AK', '')
sk = os.getenv('QIANFAN_SK', '')

print(f'AK: {ak[:20]}...' if len(ak) > 20 else f'AK: {ak}')
print(f'SK: {sk[:20]}...' if len(sk) > 20 else f'SK: {sk}')
print(f'AK 长度: {len(ak)}')
print(f'SK 长度: {len(sk)}')

if not ak or not sk:
    print('❌ AK 或 SK 未配置')
    exit(1)

print()
print('=== 1. 测试获取 access token...')

url = "https://aip.baidubce.com/oauth/2.0/token"
params = {
    "grant_type": "client_credentials",
    "client_id": ak,
    "client_secret": sk
}

try:
    response = requests.get(url, params=params, timeout=30)
    print(f'状态码: {response.status_code}')
    
    result = response.json()
    if 'access_token' in result:
        access_token = result['access_token']
        print(f'✅ 获取 access token 成功')
        print(f'   token: {access_token[:30]}...')
    else:
        print(f'❌ 获取失败')
        print(f'   错误: {result}')
        exit(1)
except Exception as e:
    print(f'❌ 请求异常: {e}')
    exit(1)

print()
print('=== 2. 测试提交图像生成任务...')

submit_url = f"https://aip.baidubce.com/rpc/2.0/ernievilg/v1/txt2img?access_token={access_token}"
headers = {"Content-Type": "application/json"}

submit_data = {
    "text": "一个美丽的日落",
    "style": "写实风格",
    "resolution": "1024*1024",
    "num": 1
}

try:
    response = requests.post(submit_url, headers=headers, json=submit_data, timeout=30)
    print(f'状态码: {response.status_code}')
    
    result = response.json()
    if 'error_code' in result:
        print(f'❌ 提交失败')
        print(f'   错误码: {result["error_code"]}')
        print(f'   错误信息: {result.get("error_msg", "未知错误")}')
        exit(1)
    
    task_id = result.get('data', {}).get('taskId')
    if task_id:
        print(f'✅ 任务提交成功')
        print(f'   taskId: {task_id}')
    else:
        print(f'❌ 响应中没有 taskId')
        print(f'   响应: {result}')
        exit(1)
except Exception as e:
    print(f'❌ 请求异常: {e}')
    exit(1)

print()
print('=== 测试完成 ===')
print('注意：图像生成需要等待，实际使用时需要轮询查询结果')
