import os
from dotenv import load_dotenv
load_dotenv()

ak = os.getenv('QIANFAN_AK', '')
sk = os.getenv('QIANFAN_SK', '')

print("=== 测试百度千帆 SDK ===")
print(f"AK: {ak[:20]}...")
print(f"SK: {sk[:20]}...")

os.environ['QIANFAN_AK'] = ak
os.environ['QIANFAN_SK'] = sk

import qianfan

print()
print("1. 测试 ChatCompletion...")
try:
    chat_comp = qianfan.ChatCompletion()
    resp = chat_comp.do(
        model="ERNIE-Lite-8K",
        messages=[{"role": "user", "content": "你好，请回复一句简单的话。"}]
    )
    body = resp.get('body', {}) if isinstance(resp, dict) else {}
    result = body.get('result', 'OK')
    print(f"   OK: {result[:50]}")
except Exception as e:
    print(f"   失败: {e}")

print()
print("2. 测试 Text2Image...")
try:
    t2i = qianfan.Text2Image()
    resp = t2i.do(
        prompt="一个美丽的日落",
        with_decode="base64",
        model="Stable-Diffusion-XL"
    )
    
    if isinstance(resp, dict):
        body = resp.get('body', {})
        data_list = body.get('data', [])
        if data_list and len(data_list) > 0:
            img_data = data_list[0].get('image')
            if img_data:
                print(f"   OK: 生成了图片，base64长度: {len(img_data)}")
                
                import base64
                with open('test_image.png', 'wb') as f:
                    f.write(base64.b64decode(img_data))
                print(f"   已保存到 test_image.png")
            else:
                print(f"   响应: {str(resp)[:200]}")
        else:
            print(f"   响应: {str(resp)[:200]}")
    else:
        print(f"   响应类型: {type(resp)}")
        
except Exception as e:
    print(f"   失败: {e}")
    import traceback
    traceback.print_exc()

print()
print("=== 测试完成 ===")
