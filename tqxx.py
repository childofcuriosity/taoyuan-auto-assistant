import mss
import sys
import time
import platform
from src.touchlink import TouchLink

# ================= 跨平台配置区 =================

# 1. 目标颜色 (R, G, B)
TARGET_COLOR = (241, 225, 143)
TOLERANCE = 40 

# 2. 【关键】屏幕绝对坐标 (不再依赖窗口自动定位)
# 请使用系统自带截图工具获取屏幕上的绝对坐标 (X, Y)
MONITOR_X = list(range(2865,4174,327))
MONITOR_Y=1535
PHONE_X= list(range(228,1373,286))
PHONE_Y=695

target_ms=600
target_ns=target_ms*1e6

# ===============================================

def color_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

def wait_for_first_pixel(sct):
    monitor_area = {
        "top": MONITOR_Y,
        "left": MONITOR_X[0],
        "width": MONITOR_X[-1] - MONITOR_X[0] + 1,
        "height": 1
    }

    print("等待像素触发作为时间基准...")

    while True:
        img = sct.grab(monitor_area)
        for i in range(5):
            x_offset = MONITOR_X[i] - MONITOR_X[0]
            r, g, b = img.pixel(x_offset, 0)[:3]
            if color_distance((r, g, b), TARGET_COLOR) < TOLERANCE:
                print(f"像素命中于 index={i}")
                return time.perf_counter_ns()


def main():
    tk = TouchLink()

    # 预构建命令（完全不变）
    cmd = []
    for i in range(5):
        cmd.append({
            'action': 'swipe',
            'args': [PHONE_X[i], PHONE_Y+2, PHONE_X[i], PHONE_Y+100],
            'duration': 400,
            'extras': {'stabilize': 0}
        })

    with mss.mss() as sct:
        # ① 等待像素 → 得到时间零点
        t0 = wait_for_first_pixel(sct)

        tk.custom(cmd)
        print("进入定时节拍循环")

        while True:
            # ② 忙等到下一个节拍
            while time.perf_counter_ns() - t0 < target_ns:
                pass

            t1 = time.perf_counter_ns()
            print(f"loop cost: {(t1 - t0) / 1e6:.3f} ms")

            # ③ 更新基准（不是用 now！）
            t0 += target_ns

            # ④ 执行动作
            tk.custom(cmd)


if __name__ == "__main__":
    main()