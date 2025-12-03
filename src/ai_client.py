# 文件: MyProject/src/ai_client.py
import os
import base64
import io
from openai import OpenAI
from PIL import Image

# === 注意：删除了全局的 _CLIENT 变量，不再缓存客户端 ===

def get_client():
    """
    每次调用都创建一个新的 OpenAI 客户端实例。
    这能有效防止长时间运行后，智谱AI的 JWT Token 过期导致的 401 错误。
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("ai_base_url", "https://open.bigmodel.cn/api/paas/v4") 

    if not api_key:
        print("【错误】未检测到 API Key，请先在配置页填写并保存！")
        # 返回 None 而不是直接报错，让调用者处理
        return None

    # 每次实例化都会根据 Key 重新计算签名，保证不过期
    return OpenAI(api_key=api_key, base_url=base_url)

def convert_image_to_webp_base64(input_image_path: str, quality: int = 80) -> str:
    """
    将本地图片压缩为 WebP 并转为 Base64。
    """
    try:
        with Image.open(input_image_path) as img:
            # 针对大分辨率进行缩放，节省 token 并加快速度
            # 如果图片宽或高超过 1024，按比例缩小
            if img.width > 1024 or img.height > 1024:
                img.thumbnail((1024, 1024))
            
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
                        "url": f"data:image/webp;base64,{b64_image}"
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
    print(f"【AI调用】正在询问图片: {prompt[:20]}...") # 只打印前20个字，防止日志太长
    
    try:
        # 1. 获取新客户端
        client = get_client()
        if not client:
            return "错误：API Key 未设置"

        # 2. 构建消息
        messages = build_messages(image_path, prompt)
        if not messages:
            return "错误：图片转换失败"

        # 3. 发起请求
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            temperature=0.1, # 降低随机性
            max_tokens=1024
        )
        
        result = response.choices[0].message.content
        # print(f"【AI回复】{result}") # 调试时可以打开，平时太吵可以注释
        return result

    except Exception as e:
        err_msg = f"AI 请求异常: {str(e)}"
        print(f"【错误】{err_msg}")
        
        # 如果是 401 错误，特意提醒一下
        if "401" in str(e):
            print(">>> 提示：API Key 可能过期或余额不足，或者 Key 填写错误。")
            
        return err_msg

# === 单元测试 ===
if __name__ == "__main__":
    pass