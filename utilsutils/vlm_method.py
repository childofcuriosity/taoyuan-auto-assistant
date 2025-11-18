import os
import base64
import io
from openai import OpenAI
from PIL import Image

# module-level client cache
_CLIENT = None


def get_client(api_key: str | None = None, base_url: str = "https://open.bigmodel.cn/api/paas/v4"):
    """
    返回一个单例 OpenAI client。多次调用会复用同一个 client，从而避免每次都慢慢创建。
    优先从参数 api_key 取值；如果没有则从环境变量 OPENAI_API_KEY 读取。
    """
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("API key 未设置：请通过参数传入或设置环境变量 OPENAI_API_KEY。")

    _CLIENT = OpenAI(api_key=key, base_url=base_url)
    return _CLIENT


def convert_image_to_webp_base64(input_image_path: str, quality: int = 85) -> str | None:
    """将本地图片转换为 WebP 并返回 base64 字符串（不包含 data: 前缀）"""
    try:
        with Image.open(input_image_path) as img:
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='WEBP', quality=quality)
            return base64.b64encode(byte_arr.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"[convert_image_to_webp_base64] 图片转换错误: {e}")
        return None


def build_prompt(image_path: str,instruction_text: str) -> list:
    """
    构建发送给 VLM 的 messages 列表（与参考代码结构一致）。
    注意：这里把图片直接转换为 data:image/webp;base64,... 并把提示语放在同一个 user 消息里（模型可根据具体实现调整）。
    """
    print("【查看】制作 prompt")
    b64 = convert_image_to_webp_base64(image_path)
    if not b64:
        raise RuntimeError("图片转换失败，无法构建 prompt。")
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/webp;base64,{b64}",
                        "detail": "high"
                    }
                },
                {
                    "type": "text",
                    "text": instruction_text
                }
            ]
        }
    ]

    return messages




def send_to_vlm(messages: list, model: str = 'glm-4.1v-thinking-flash', max_tokens: int = 10000, api_key: str | None = None):
    """
    使用参考代码的流式方式调用 VLM（chat completion），并返回解析后的结果。
    messages: build_prompt 返回的 messages 列表
    返回值：解析后的标签（"harvest"/"growing"/"empty"）或无法解析时的原始文本
    """
    print("【查看】发送给 VLM 等待返回")
    client = get_client(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        max_tokens=max_tokens
    )
    full_response = response.choices[0].message.content
    print(f"【查看】VLM 返回完整内容：{full_response}")
    return full_response    


# ------- usage example -------
if __name__ == "__main__":
    # 推荐：在环境变量里设置 OPENAI_API_KEY，避免把密钥硬编码到文件中
    image_path = "adb_screen.png"  # 替换为实际路径
    prompt = build_prompt(image_path,'test')           # 符合你原来逻辑：先 build_prompt
    vlm_result = send_to_vlm(prompt)            # 再 send_to_vlm
    print("VLM 最终结果 ->", vlm_result)
    # 智谱官方很快。

