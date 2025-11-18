from farming.farming_utils import *

def start_check():
    print("【查看】开始")
    return True

def extract_value(text):
    print("【查看】提取 VLM 返回值")
    t = text.lower().strip()
    # 直接精确匹配或包含关键字
    if re.search(r'\bharvest\b', t):
        return "harvest"
    if re.search(r'\bgrowing\b', t):
        return "growing"
    if re.search(r'\bempty\b', t):
        return "empty"
    return text.strip()


def end_check():
    print("【查看】结束")
    return True


def check_status():

    zoom_and_locate()
    tap_field()
    start_check()
    image_path = screenshot()   

    instruction_text = (
        "请识别这张图的作物状态。**只**在三个选项中返回一个单词（小写）："
        "`harvest`（可收割，判定依据是有镰刀）, `growing`（生长中，判定依据是有时间条）,`empty`（空闲，判定依据是有作物列表）。"
        "不要输出其他多余说明。"
    )
    prompt = build_prompt(image_path, instruction_text)
    vlm_response = send_to_vlm(prompt)

    status = extract_value(vlm_response)
    end_check()

    return status


if __name__ == "__main__":

    
    print(check_status())