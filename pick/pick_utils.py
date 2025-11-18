from utils import *
def extract_value(text):
    print("【查看】提取 VLM 返回值")
    t = text.lower().strip()
    # 直接精确匹配或包含关键字
    if re.search(r'\bharvest\b', t):
        return "harvest"
    if re.search(r'\bpicking\b', t):
        return "picking"
    if re.search(r'\bempty\b', t):
        return "empty"
    return text.strip()

def check_status():
    image_path = screenshot()   

    instruction_text = (
        "请识别这张图的生产状态。**只**在三个选项中返回一个单词（小写）："
        "`harvest`（可收获，判定依据是有已完成、收获的字样）, `picking`（采集中，判定依据是有剩余时间、加速的字样）,`empty`（空闲，判定依据是有开始生产字样）。"
        "不要输出其他多余说明。"
    )
    prompt = build_prompt(image_path, instruction_text)
    vlm_response = send_to_vlm(prompt)

    status = extract_value(vlm_response)

    return status

def extract_pick(text,goods_list):
    print("【采集判断】提取 VLM 返回值")

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
    for crop in goods_list:
        if crop in t:
            return crop


    # ---------- 6. 最终兜底 ----------
    return "无"

def decide_pick(goods_list,num_param=20):
    num = num_param or int(os.environ.get("plant_num_limit"))
    print("决定采集什么")
    img_path = screenshot()
    instruction = f"界面右上角的从左到右作物依次是{str(goods_list)}，物品右下角数字表示库存个数。请你找到库存最少的作物个数是否少于{num}个，如果是请返回该作物名称，如果否那就返回\"无\"，不要有其他多余说明。"
    prompt = build_prompt(img_path, instruction)
    vlm_response = send_to_vlm(prompt)
    result = extract_pick(vlm_response,goods_list)
    return result

def pick_action(goods_list,seed_type):
    print(f"采集：{seed_type}")
    # 这里添加实际的采集和种植操作代码
    ry=0.2159
    # 找到 seed_type 在 goods_list 中的下标 i
    i = goods_list.index(seed_type)
    # 计算 rx
    rx = 0.6518 + (0.8705 - 0.6518) / 3 * i
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(rx, ry)  # 点击采集的东西
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.7821, 0.8476)  # 点击开始生产按钮
    time.sleep(eval(os.environ.get("small_delay")))
    return True



def handle_area(goods_list):
    status = check_status()
    print("处理区域，状态为：", status)
    if status == "picking":
        return True
    elif status == "harvest" or status == "empty":
        if status == "harvest":
            click_ratio(0.7821, 0.8476)  # 点击收获按钮
        need = decide_pick(goods_list)

        if need == "无":
            return True

        # need 为作物名称
        pick_action(goods_list,seed_type=need)
        return True
    else:
        print("【采集】未知状态，直接结束")
        return True