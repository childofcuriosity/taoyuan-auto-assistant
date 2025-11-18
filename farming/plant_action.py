from farming.farming_utils import *


RX_START = 0.2152
RX_END   = 0.8125
RY_CONST = 0.839

def plant_action(seed_type):
    print("【种地】播种中：", seed_type)

    if seed_type not in CROP_LIST:
        print(f"错误：未知种子类型 {seed_type}")
        return True

    # 计算 index
    idx = CROP_LIST.index(seed_type)

    # 8 个点 → 7 段，等分
    step = (RX_END - RX_START) / (len(CROP_LIST) - 1)

    # 得到该 seed_type 的 rx
    rx = RX_START + idx * step
    ry = RY_CONST

    # 执行操作
    use4field(rx, ry)
    return True

if __name__ == "__main__":
    plant_action("土豆")
    print(1)
