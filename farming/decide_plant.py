from farming.farming_utils import *
import time


# ================================
#  1. 入口函数
# ================================

def start_decide():
    print("【播种判断】开始")
    return True


def end_decide():
    print("【播种判断】结束")
    return True

def extract_value(text):
    """
    从 VLM 返回文本中提取结果（更加鲁棒版本）
        - 优先精准匹配作物名称
        - 能处理各种包装字符：如 <|xxx|>、符号、解释性文字
        - 未识别返回 "无"
    """
    print("【播种判断】提取 VLM 返回值")

    if not text or text.strip() == "":
        return "无"

    t = text.strip()

    # ---------- 1. 统一处理 None/null ----------
    if t.lower() in ["none", "null"]:
        return "无"

    # ---------- 2. 去掉常见 VLM 包装符 ----------
    # 类似 <|begin_of_box|>甘蔗<|end_of_box|>
    for p in ["<|begin_of_box|>", "<|end_of_box|>", "<|box|>", "<|", "|>"]:
        t = t.replace(p, "")

    # ---------- 3. 去掉奇怪符号 ----------
    # 保留中文、英文、数字
    t = re.sub(r"[^\w\u4e00-\u9fff]", " ", t)
    t = t.strip()

    # ---------- 4. 在字符串里搜索是否包含某作物 ----------
    for crop in CROP_LIST:
        if crop in t:
            return crop

    # ---------- 5. 单独处理英文 crop 名字 ----------
    # 允许 VLM 输出英文 (例如 potato)
    EN2CN = {
        "wheat": "小麦",
        "soybean": "大豆",
        "sugarcane": "甘蔗",
        "rice": "水稻",
        "cabbage": "白菜",
        "chili": "辣椒",
        "pepper": "辣椒",
        "potato": "土豆",
        "ramie": "苎麻",
    }

    low = t.lower()
    for en, cn in EN2CN.items():
        if en in low:
            return cn

    # ---------- 6. 最终兜底 ----------
    return "无"
# ================================
# 2. 双截图 + 拼接
# ================================

def double_screenshot():
    """
    截两次图 + 拼接（如果你需要）
    返回最终图片路径
    """
    print("【播种判断】双截图流程")

    img1 = screenshot("plant_check_1.png")
    time.sleep(eval(os.environ.get("small_delay")))
    drag_ratio(0.6393,0.9119,0.4071,0.9230)
    time.sleep(eval(os.environ.get("small_delay")))
    img2 = screenshot("plant_check_2.png")
    time.sleep(eval(os.environ.get("small_delay")))
    drag_ratio(0.4071,0.9230,0.6393,0.9119)
    time.sleep(eval(os.environ.get("small_delay")))
    # 如需拼接，可在这里做
    final_path = "plant_check_final.png"
    splice_images(img1, img2, final_path,0.6,0.52)

    return final_path

def splice_images(path1, path2, out_path, left_ratio, right_ratio):
    """
    按比例拼接两张截图：
      - 从第一张图取左侧 left_ratio 比例（0~1）
      - 从第二张图取右侧 right_ratio 比例（0~1）

    示例：
      left_ratio=0.6  → 取第一张的左 60%
      right_ratio=0.6 → 取第二张的右 60%

    最终拼接宽度 = left_crop_width + right_crop_width
    """
    from PIL import Image

    img1 = Image.open(path1)
    img2 = Image.open(path2)

    h = max(img1.height, img2.height)

    # ---- 第一张：左侧 left_ratio ----
    w1 = img1.width
    left_crop_width = int(w1 * left_ratio)
    left_crop = img1.crop((0, 0, left_crop_width, img1.height))

    # ---- 第二张：右侧 right_ratio ----
    w2 = img2.width
    right_crop_width = int(w2 * right_ratio)
    right_crop = img2.crop((w2 - right_crop_width, 0, w2, img2.height))

    # ---- 拼接 ----
    combined = Image.new("RGB", (left_crop_width + right_crop_width, h))
    combined.paste(left_crop, (0, 0))
    combined.paste(right_crop, (left_crop_width, 0))
    combined.save(out_path)

    return out_path



# ================================
# 3. 核心逻辑：判断是否播种
# ================================

def decide_plant(num_param=None):
    num = num_param or int(os.environ.get("plant_num_limit"))
    """
    主流程（完全对应流程图）：

        start_decide
        → zoom_and_locate
        → tap_field
        → screenshot ×2
        → splice
        → build_prompt
        → send_to_vlm
        → extract_value
        → end_decide
        → 返回 'yes' / 'no'
    """

    start_decide()

    # 放大缩小并定位：完全复用 check_status 的函数
    zoom_and_locate()

    # 点按田地
    tap_field()

    # 双截图 + 拼接
    final_path = double_screenshot()

    # 提示词（你自己可修改）
    instruction = f"从左到右作物依次是小麦、大豆、甘蔗、水稻、白菜、辣椒、土豆、苎麻，作物下面数字表示库存个数。请你找到库存最少的作物个数是否少于{num}个，如果是请返回该作物名称，如果否那就返回\"无\"，不要有其他多余说明。"

    prompt = build_prompt(final_path, instruction)
    vlm_response = send_to_vlm(prompt)

    result = extract_value(vlm_response)
    print(f"【播种判断】VLM 返回结果：{result}")
    end_decide()

    return result


if __name__ == "__main__":
    result = decide_plant()

    if result != "无":
        print(f"【自动补货】需要播种 → 作物：{result}")
    else:
        print("【自动补货】不需要播种")
