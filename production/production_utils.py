from utils import *


def try_harvest():
    print("尝试收获")
    ry = 0.9000
    start = 0.1335
    end = 0.5241
    # 生成 6 个等距点
    x_list = [start + i * (end - start) / 5 for i in range(6)]
    for rx in reversed(x_list):
        click_ratio(rx, ry)  # 点击收获按钮
        time.sleep(eval(os.environ.get("small_delay")))
        click_ratio(0.8183, 0.4619)  # 可能未解锁就要退出
        time.sleep(eval(os.environ.get("small_delay")))
    return True
import re

def parse_vlm_inventory(vlm_response: str):
    """
    对 VLM 返回的库存列表做后处理。
    要求格式如：[1, 23, 5, 18]
    使用正则提取数字并返回 int 列表。
    
    如果格式不符合或没有数字，返回原始 vlm_response 字符串。
    """
    # 匹配方括号内的内容
    pattern = r'\[\s*(.*?)\s*\]'
    match = re.search(pattern, vlm_response)


    if not match:
        return vlm_response  # 格式不符，直接返回原文

    inner = match.group(1)

    # 匹配所有整数（允许空格）
    nums = re.findall(r'-?\d+', inner)

    if not nums:
        return vlm_response  # 没有数字，返回原文

    # 转成 int 列表
    return [int(n) for n in nums]

import re
from typing import List, Optional,Tuple

def find_product_name_in_text(text: str, goods_list: List[str]) -> Optional[str]:
    """
    从 text 中找到 goods_list 里的商品名，返回匹配到的名称。
    商品名都是连续汉字词。
    """
    t = text.strip()

    for name in reversed(goods_list):# 优先匹配后面的名称，防止糖和红糖等混淆
        if re.search(name, t):
            return name

    return None

def process_slot_response_and_update(
        vlm_resp: str,
        goods_list: List[str],
        goods_nums: List[int],
        empty_count: int
    ) -> Tuple[List[int], int]:

    resp = (vlm_resp or "").strip()

    # 1) 是否为空的 —— 正则判断
    if re.search(r"空的", resp):
        empty_count += 1
        return goods_nums, empty_count

    # 2) 查找商品名
    name = find_product_name_in_text(resp, goods_list)

    if name is not None:
        idx = goods_list.index(name)
        goods_nums[idx] += 1

    return goods_nums, empty_count


def figure_state(goods_list):
    image_path = screenshot()  

    create_white_image_like(image_path, "white.png")
    ratio1 = (0.6054, 0.1619, 0.8933, 0.4056)  # 左 20%
    # (left_ratio, top_ratio, right_ratio, bottom_ratio)
    copy_rectangle_by_ratio(ratio1, image_path, "white.png", "output1.png")
    instruction = f"界面右上角从上到下看有2行，每一行里面从左到右看，这样子看到的产品名称依次是{str(goods_list)}。"
    instruction1="每个产品右下角数字表示库存个数，请你识别每个产品的库存个数并且作为列表返回，格式为[第1个产品的个数,...,第n个产品的个数]，n产品名称的种数。不要有其他多余说明。"

    prompt1 = build_prompt("output1.png", instruction + instruction1)
    vlm_response1 = send_to_vlm(prompt1)
    goods_nums=parse_vlm_inventory(vlm_response1)
    if isinstance(goods_nums, str) or len(goods_nums)!=len(goods_list):
        print(f"【生产】VLM 返回无法解析的结果：{goods_nums}")
        return [], 0
    print(f"【生产】识别到的库存列表：{goods_nums}")

    instruction2="界面下方有一个格子，里面如果是空的就返回'空的'，是'可解锁'字样就返回'可解锁'，否则返回该产品名称，不要有其他多余说明。"
    ST=0.0844
    ED=0.5661
    DETA=(ED-ST)/6
    ratio2 = (ST, 0.8286, ST+DETA, 0.9675)
    empty_count = 0  
    for i in range(6):
        copy_rectangle_by_ratio(ratio2, image_path, "output1.png", f"output2{i}.png")
        prompt2 = build_prompt(f"output2{i}.png", instruction + instruction2)
        vlm_response2 = send_to_vlm(prompt2)
        goods_nums, empty_count = process_slot_response_and_update(
            vlm_response2, goods_list, goods_nums, empty_count
        )
        ratio2 = (ratio2[0]+DETA, ratio2[1], ratio2[2]+DETA, ratio2[3])
    
    print(f"【生产】识别到的库存+队列列表：{goods_nums}")
    print(f"【生产】识别到的可生产格子数量：{empty_count}")
    return goods_nums, empty_count

def produce_good(idx):
    print(f"生产第 {idx} 个商品")
    row=idx//4
    col=idx%4
    xST=0.6446
    yST=0.2262
    xED=0.8603
    yED=0.3563
    rx=xST+(xED-xST)/3*col
    ry=yST+(yED-yST)*row
    click_ratio(rx, ry)  # 点击采集的东西
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.7821, 0.8476)  # 点击开始生产按钮
    time.sleep(eval(os.environ.get("small_delay")))
    return True

def try_produce(goods_nums, empty_count,num):
    """
    goods_nums: 列表，每个元素代表当前的库存量
    empty_count: 要补货的次数
    """
    for _ in range(empty_count):
        # 找到最小值索引
        idx = goods_nums.index(min(goods_nums))
        if goods_nums[idx]>=num:
            print("所有商品库存均已充足，无需生产")
            return True
        # 调用函数
        produce_good(idx)
        
        # 自增
        goods_nums[idx] += 1


def handle_area(goods_list, num_param=None):
    num = num_param or int(os.environ.get("produce_num_limit"))
    try_harvest()
    goods_nums, empty_count=figure_state(goods_list)
    if goods_nums==[]:
        return True
    try_produce(goods_nums, empty_count, num)


    return True
if __name__ == "__main__":
    goods_list=['陶艺木具','榫卯','鲁班锁']
    handle_area(goods_list)