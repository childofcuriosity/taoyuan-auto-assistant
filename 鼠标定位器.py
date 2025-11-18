from config import *
import pygetwindow as gw
import pyautogui
import time
import os

# 找窗口
window_title = os.environ['window_name']
window = gw.getWindowsWithTitle(window_title)[0]

print(f"检测到窗口：{window_title}")
print("按 Ctrl+C 停止\n")

while True:
    # 当前鼠标绝对坐标
    mx, my = pyautogui.position()

    # 判断鼠标是否在窗口区域内
    if window.left <= mx <= window.right and window.top <= my <= window.bottom:

        # 窗口内相对坐标
        x_rel = mx - window.left
        y_rel = my - window.top

        # 转比例
        rx = x_rel / window.width
        ry = y_rel / window.height

        # 清屏（为了让输出更清晰）
        os.system("cls")

        print("鼠标在窗口内")
        print(f"窗口位置：({window.left}, {window.top})")
        print(f"窗口大小：{window.width} × {window.height}\n")

        print(f"鼠标绝对坐标：({mx}, {my})")
        print(f"鼠标窗口坐标：({x_rel}, {y_rel})")
        print(f"鼠标窗口比例：({rx:.4f}, {ry:.4f})")
    else:
        os.system("cls")
        print("鼠标不在窗口内")

    time.sleep(eval(os.environ.get("small_delay")))
