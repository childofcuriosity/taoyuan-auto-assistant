import mss
import sys
import time
import platform
from src.touchlink import TouchLink

# ================= 跨平台配置区 =================

# 1. 目标颜色 (R, G, B)
TARGET_COLOR = (241, 225, 143)
TOLERANCE = 50

# 2. 【关键】屏幕绝对坐标 (不再依赖窗口自动定位)
# 请使用系统自带截图工具获取屏幕上的绝对坐标 (X, Y)
MONITOR_X = list(range(2865,4174,327))
MONITOR_Y=1535
PHONE_X= list(range(228,1373,286))
PHONE_Y=695

# ===============================================

def color_distance(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

def main():
    tk=TouchLink()
    with mss.mss() as sct:
        monitor_area = {
            "top": MONITOR_Y,
            "left": MONITOR_X[0],
            "width": MONITOR_X[-1] - MONITOR_X[0] + 1,
            "height": 1
        }
        try:
            t0=time.perf_counter_ns()
            while True:
                cmd=[]
                img = sct.grab(monitor_area)
                for i  in range(5):
                    x_offset= MONITOR_X[i]- MONITOR_X[0]
                    current_pixel = img.pixel(x_offset, 0)
                    
                    r, g, b = current_pixel[0], current_pixel[1], current_pixel[2]
                    
                    diff = color_distance((r, g, b), TARGET_COLOR)
                    if diff<TOLERANCE:
                        cmd.append({ 'action': 'swipe', 'args': [PHONE_X[i], PHONE_Y+2, PHONE_X[i],  PHONE_Y+10], 'duration': 1, 'extras': {'stabilize': 0} })

                if cmd!=[]:
                    tk.custom(cmd)


        except KeyboardInterrupt:
            print("\n已停止监控。")
        except Exception as e:
            print(f"发生错误: {e}")
            # macOS如果没给权限，通常会报 ScreenShotError

if __name__ == "__main__":
    main()