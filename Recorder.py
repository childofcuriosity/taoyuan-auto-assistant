import mss
import time
import json
import math
from datetime import datetime

# === 引入配置 ===
# (这里请粘贴上面的配置变量)
# ... TARGET_COLOR, MONITOR_X 等 ...
from config import *

def color_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

def wait_for_start(sct):
    print("等待开始信号...")
    while True:
        # 抓取开始信号的一个像素
        img = sct.grab({"top": START_SIGNAL_POS[1], "left": START_SIGNAL_POS[0], "width": 1, "height": 1})
        pixel = img.pixel(0, 0)
        if color_distance(pixel, START_SIGNAL_COLOR) < START_TOLERANCE:
            print(">>> 捕捉到开始信号！计时开始！ <<<")
            return time.perf_counter_ns()
        time.sleep(0.01)

def record():
    # 记录的数据列表
    actions = []
    # 记录每条轨道的最后触发时间，用于防抖
    last_trigger_time = {i: 0 for i in range(len(MONITOR_X))}

    with mss.mss() as sct:
        # 定义监控区域 (长条形区域覆盖所有点)
        monitor_area = {
            "top": MONITOR_Y,
            "left": MONITOR_X[0],
            "width": MONITOR_X[-1] - MONITOR_X[0] + 1,
            "height": 1
        }

        # 1. 等待开始
        t0 = wait_for_start(sct)

        print("正在录制... 按 Ctrl+C 停止并保存")
        try:
            while True:
                current_time_ns = time.perf_counter_ns()
                elapsed_ms = (current_time_ns - t0) / 1_000_000 # 转换为毫秒

                img = sct.grab(monitor_area)

                for i in range(len(MONITOR_X)):
                    # 计算该点在截图中的相对X坐标
                    x_offset = MONITOR_X[i] - MONITOR_X[0]
                    pixel = img.pixel(x_offset, 0)
                    r, g, b = pixel[0], pixel[1], pixel[2]

                    if color_distance((r, g, b), TARGET_COLOR) < TOLERANCE:
                        # 检查冷却时间
                        if (elapsed_ms - last_trigger_time[i]) > COOLDOWN_MS:
                            # 记录动作
                            action = {
                                "time_ms": int(elapsed_ms), # 相对毫秒数
                                "lane_index": i,            # 轨道索引 0-4
                                "type": "tap"               # 预留扩展类型
                            }
                            actions.append(action)
                            print(f"记录: 轨道 {i} @ {int(elapsed_ms)}ms")
                            
                            # 更新该轨道的冷却时间
                            last_trigger_time[i] = elapsed_ms
                
                # 极短休眠防止CPU 100%，但要保持高频采样
                # time.sleep(0.001) 

        except KeyboardInterrupt:
            print("\n录制停止。正在保存 timeline.json ...")
            # 按时间排序，确保顺序正确
            actions.sort(key=lambda x: x["time_ms"])
            
            with open("timeline.json", "w", encoding="utf-8") as f:
                json.dump(actions, f, indent=4)
            print(f"保存成功，共记录 {len(actions)} 个动作。请打开文件进行微调。")

if __name__ == "__main__":
    record()