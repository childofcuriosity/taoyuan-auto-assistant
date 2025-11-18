from utils import *
def extract_int(text):
    """
    从 text 中提取第一个整数。
    可兼容情况:
        - "123"
        - " \box{123} "
        - "[6]"
        - "<|begin_of_box|>8<|end_of_box|>"
        - "result is 7"
        - "abc 42 xyz"
    """
    if text is None:
        return None

    t = text.strip()

    # 匹配第一个整数（包含负数情况）
    m = re.search(r'-?\d+', t)
    if not m:
        return None  # 没有数字
    return int(m.group())

def process(rx,ry,tag,num_limit):
    print(f"处理{tag}")
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(rx, ry)
    time.sleep(eval(os.environ.get("small_delay")))
    image_path = screenshot()  
    rectangle_ratio=(0.1777, 0.4254, 0.2460, 0.4643)
    copy_rectangle_by_ratio(rectangle_ratio, image_path,  "white.png", "outputSALE.png")
    instruction = f"识别一下数字，直接返回该数字，不要有其他多余说明。"
    prompt = build_prompt("outputSALE.png", instruction)
    vlm_response = send_to_vlm(prompt)
    print(f"VLM返回结果：{vlm_response}")
    try:
        num = extract_int(vlm_response)
    except ValueError:
        print(f"无法解析的数字：{vlm_response}")
        return False
    
    if num<num_limit:
        print(f"{tag} 数量 {num} 小于限制 {num_limit}，结束处理")
        return False
    print(f"{tag} 数量 {num} 大于等于限制 {num_limit}，继续处理")
    
    time.sleep(eval(os.environ.get("small_delay")))     
    click_ratio(0.2100, 0.3600)  # 点击处理按钮
    
    time.sleep(eval(os.environ.get("small_delay")))     
    click_ratio(0.2147, 0.6452)  # 点击处理按钮
    time.sleep(eval(os.environ.get("big_delay")))     
    click_ratio(0.2147, 0.7114)  # 点击处理按钮（对比较长的来说）
    time.sleep(eval(os.environ.get("big_delay")))     
    click_ratio(0.2147, 0.7814)  # 点击处理按钮（对比较长的来说）
    time.sleep(eval(os.environ.get("big_delay")))     
    click_ratio(0.5978, 0.6897)  # 点击确认按钮
    time.sleep(eval(os.environ.get("big_delay")))     
    return True
    
    