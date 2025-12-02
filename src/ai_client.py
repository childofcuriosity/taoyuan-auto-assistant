# 文件: MyProject/src/ai_client.py
import os
import base64
import io
from openai import OpenAI
from PIL import Image

# 单例缓存，避免重复创建连接
_CLIENT = None

def get_client():
    """
    获取 OpenAI 客户端单例。
    自动从 os.environ 读取 'OPENAI_API_KEY' (由 logic.py 注入)。
    """
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("ai_base_url", "https://open.bigmodel.cn/api/paas/v4") # 默认智谱

    if not api_key:
        print("【错误】未检测到 API Key，请先在配置页填写并保存！")
        raise RuntimeError("Environment variable OPENAI_API_KEY is missing")

    _CLIENT = OpenAI(api_key=api_key, base_url=base_url)
    return _CLIENT

def convert_image_to_webp_base64(input_image_path: str, quality: int = 80) -> str:
    """
    将本地图片压缩为 WebP 并转为 Base64。
    WebP 格式通常比 PNG/JPG 小很多，能加快上传速度并节省 Tokens。
    """
    try:
        with Image.open(input_image_path) as img:
            # 如果图片太大，可以考虑缩小，例如：
            # img.thumbnail((1024, 1024)) 
            
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='WEBP', quality=quality)
            return base64.b64encode(byte_arr.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"【图片处理错误】无法读取或转换图片: {input_image_path}, 错误: {e}")
        return None

def build_messages(image_path: str, prompt_text: str):
    """构建发送给大模型的标准消息体"""
    b64_image = convert_image_to_webp_base64(image_path)
    if not b64_image:
        return None

    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/webp;base64,{b64_image}",
                        "detail": "high" # 智谱GLM通常不需要这个参数，但为了兼容OpenAI格式保留
                    }
                },
                {
                    "type": "text",
                    "text": prompt_text
                }
            ]
        }
    ]

def query_vlm(image_path: str, prompt: str, model: str = 'glm-4v-flash'):
    """
    [核心对外接口]
    输入：图片路径、提示词
    输出：大模型的文本回答
    """
    print(f"【AI调用】正在询问图片: {prompt}...")
    
    try:
        client = get_client()
        messages = build_messages(image_path, prompt)
        if not messages:
            return "错误：图片转换失败"

        # 发起请求
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            temperature=0.1, # 降低随机性，让回答更稳定
            max_tokens=1024
        )
        
        result = response.choices[0].message.content
        print(f"【AI回复】{result}")
        return result

    except Exception as e:
        err_msg = f"AI 请求异常: {str(e)}"
        print(f"【错误】{err_msg}")
        return err_msg

# === 单元测试 ===
if __name__ == "__main__":
    # 在这里手动设置 Key 测试一下
    # os.environ["OPENAI_API_KEY"] = "你的Key"
    # res = query_vlm("test.png", "这张图里有什么？")
    # print(res)
    pass