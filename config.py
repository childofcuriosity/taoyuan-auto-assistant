# config.py (或者直接复制到脚本开头)

# 1. 目标颜色 (R, G, B) - 音符的颜色
TARGET_COLOR = (241, 225, 143)
TOLERANCE = 50

# 2. 开始信号配置 (用来确定 t0)
# 请找一个游戏开始时必然会出现的固定颜色点 (例如右上角的暂停键，或者分数的颜色)
START_SIGNAL_POS = (2680, 805)  # (X, Y) 屏幕绝对坐标
START_SIGNAL_COLOR = (225, 227, 199) # 开始信号的颜色
START_TOLERANCE = 10

# 3. 坐标配置
MONITOR_X = list(range(2865, 4174, 327))
MONITOR_Y = 1535
PHONE_X = list(range(228, 1373, 286))
PHONE_Y = 695

# 4. 录制防抖动 (非常重要)
# 同一个轨道检测到音符后，多少毫秒内不再记录？避免一个音符被记录几十次
COOLDOWN_MS = 300

SCREENSHOT_DIR = "debug_screenshots"
GLOBAL_OFFSET=0