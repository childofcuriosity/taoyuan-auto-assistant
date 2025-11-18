import pygetwindow as gw
import pyautogui
import time

# -------------------------
# 绑定窗口
# -------------------------
window = gw.getWindowsWithTitle("MuMu安卓设备")[0]

# -------------------------
# 基础函数：将比例坐标转换成屏幕绝对坐标
# -------------------------
def ratio_to_abs(rx, ry):
    w = window.width
    h = window.height
    x_abs = window.left + int(w * rx)
    y_abs = window.top + int(h * ry)
    return x_abs, y_abs

# -------------------------
# 1. 移动鼠标（不点击）
# -------------------------
def move_ratio(rx, ry, duration=0.5):
    x, y = ratio_to_abs(rx, ry)
    pyautogui.moveTo(x, y, duration=duration)

# -------------------------
# 2. 点击（左键/右键）
# -------------------------
def click_ratio(rx, ry, button="left"):
    x, y = ratio_to_abs(rx, ry)
    pyautogui.click(x, y, button=button)

# -------------------------
# 3. 滚轮（向上/向下）
# -------------------------
def scroll_ratio(amount, rx=0.5, ry=0.5):
    """
    amount > 0 → 向上滚动
    amount < 0 → 向下滚动
    默认在窗口中间滚动
    """
    x, y = ratio_to_abs(rx, ry)
    pyautogui.moveTo(x, y)
    pyautogui.scroll(amount)

# -------------------------
# 4. 拖拽（从比例点 A -> 比例点 B）
# -------------------------
def drag_ratio(rx1, ry1, rx2, ry2, duration=1):
    x1, y1 = ratio_to_abs(rx1, ry1)
    x2, y2 = ratio_to_abs(rx2, ry2)
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=duration)
    pyautogui.mouseUp()

# 拆
def mouse_down_ratio(rx, ry, button="left"):
    x, y = ratio_to_abs(rx, ry)
    pyautogui.moveTo(x, y)
    pyautogui.mouseDown(button=button)

def mouse_up_ratio(button="left"):
    pyautogui.mouseUp(button=button)


# -------------------------
# 5. 按键组合（如 ctrl + scroll 或 ctrl + shift + s）
# -------------------------
def key_combo(*keys):
    """
    key_combo('ctrl', 'shift', 's')
    """
    pyautogui.hotkey(*keys)

# -------------------------
# 6. Ctrl 滚轮（浏览器缩放那种）
# -------------------------
def ctrl_scroll_ratio(amount, rx=0.5, ry=0.5, step=10, delay=0.1):
    x, y = ratio_to_abs(rx, ry)
    pyautogui.moveTo(x, y)

    pyautogui.keyDown('ctrl')
    time.sleep(delay)

    # 把大滚轮分成几个小滚动
    steps = amount // step
    for _ in range(abs(steps)):
        pyautogui.scroll(step if amount > 0 else -step)
        time.sleep(delay)

    pyautogui.keyUp('ctrl')

import subprocess
from PIL import Image
from io import BytesIO
import os

ADB_PATH = os.environ['adb_path']

def adb(cmd):
    return subprocess.run(
        [ADB_PATH] + cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    ).stdout.decode()

def adb_screenshot(path="adb_screen.png"):
    # 检查设备状态
    devices = adb(["devices"])
    if "offline" in devices.lower():
        print("ADB offline，尝试重启...")
        adb(["kill-server"])
        adb(["start-server"])
        time.sleep(1)
        devices = adb(["devices"])
        print(devices)

    # 截图
    result = subprocess.run(
        [ADB_PATH, "exec-out", "screencap", "-p"],
        stdout=subprocess.PIPE
    )

    # 如果不是 PNG，打印内容给你看
    if not result.stdout.startswith(b"\x89PNG"):
        print("ADB 返回异常：", result.stdout[:200])
        raise RuntimeError("ADB screenshot failed")

    img = Image.open(BytesIO(result.stdout))
    img.save(path)
    return img


if __name__ == "__main__":
    # 测试代码
    # move_ratio(0.5, 0.5)
    # click_ratio(0.9, 0.9)
    # scroll_ratio(-300)
    # ctrl_scroll_ratio(500)     # 放大
    # drag_ratio(0.5, 0.5, 0.8, 0.5)

    adb_screenshot()
    adb_screenshot()