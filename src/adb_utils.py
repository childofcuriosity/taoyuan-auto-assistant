# 文件: MyProject/src/adb_utils.py
import subprocess
from PIL import Image
from io import BytesIO
import os
import time

# 全局变量：存储当前选中的设备 ID
CURRENT_DEVICE_ID = None

def get_adb_path():
    """获取 ADB 路径，带默认值防止报错"""
    return os.environ.get('adb_path', 'adb')
def auto_select_device():
    """
    [核心逻辑] 自动寻找并锁定第一个可用的设备
    如果列表为空，会自动尝试连接 MuMu 的常见端口
    """
    global CURRENT_DEVICE_ID
    
    if CURRENT_DEVICE_ID:
        return CURRENT_DEVICE_ID

    adb_path = get_adb_path()
    
    # === 定义常见模拟器端口 ===
    # 7555: MuMu 6 / MuMu Pro
    # 16384: MuMu 12 (nx_main)
    # 5555: 蓝叠 / 雷电等通用端口
    mumu_ports = ["127.0.0.1:16384", "127.0.0.1:7555", "127.0.0.1:5555"]

    def check_devices():
        """内部函数：运行 adb devices 并解析"""
        try:
            res = subprocess.run(
                [adb_path, "devices"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=5
            )
            output = res.stdout.decode('utf-8', errors='ignore')
            lines = output.strip().split('\n')
            for line in lines:
                if "List of devices" in line or not line.strip():
                    continue
                parts = line.split()
                if len(parts) >= 2 and parts[1] == 'device':
                    return parts[0] # 返回设备ID
        except:
            pass
        return None

    # 1. 第一次检查
    device_id = check_devices()
    if device_id:
        CURRENT_DEVICE_ID = device_id
        print(f"【ADB】已自动锁定设备: {CURRENT_DEVICE_ID}")
        return CURRENT_DEVICE_ID

    # 2. 如果没找到，尝试主动连接 MuMu 端口
    print("【ADB】未找到设备，尝试自动连接 MuMu 模拟器端口...")
    for port in mumu_ports:
        print(f" -> 尝试连接 {port} ...")
        subprocess.run([adb_path, "connect", port], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 3. 连接后再次检查
    time.sleep(1) # 等一秒让连接生效
    device_id = check_devices()
    if device_id:
        CURRENT_DEVICE_ID = device_id
        print(f"【ADB】重连成功！锁定设备: {CURRENT_DEVICE_ID}")
        return CURRENT_DEVICE_ID
    
    print("【ADB警告】尝试连接失败，请检查模拟器是否启动，或手动执行 adb connect")
    return None
# ================= 基础 ADB 封装 =================

def run_adb_cmd(cmd_list):
    """
    执行 ADB 命令。
    自动添加 -s <device_id> 参数以解决多设备冲突。
    """
    adb_path = get_adb_path()
    
    # 1. 确保有设备ID
    device_id = auto_select_device()
    
    # 2. 构建命令前缀
    # 如果找到了设备ID，就拼装：adb -s emulator-5554 shell ...
    # 如果没找到，就裸奔：adb shell ... (可能会报错 more than one device)
    base_cmd = [adb_path]
    if device_id:
        base_cmd.extend(["-s", device_id])
        
    final_cmd = base_cmd + cmd_list
    
    try:
        result = subprocess.run(
            final_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=15 # 指令超时时间
        )
        return result.stdout.decode('utf-8', errors='ignore')
    except subprocess.TimeoutExpired:
        print(f"【ADB超时】指令: {cmd_list}")
        return ""
    except Exception as e:
        print(f"【ADB错误】{e}")
        return ""
# 文件: MyProject/src/adb_utils.py

def adb_screenshot(path="adb_screen.png", crop_box=None):
    """
    截图 (适配多设备)
    crop_box: (left, top, right, bottom) 传入元组则裁剪，不传则全图
    """
    adb_path = get_adb_path()
    device_id = auto_select_device()
    
    # 构建截图命令
    cmd = [adb_path]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "screencap", "-p"]) 
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        
        if not result.stdout.startswith(b"\x89PNG"):
            print(f"【截图失败】数据异常: {result.stdout[:20]}")
            global CURRENT_DEVICE_ID
            CURRENT_DEVICE_ID = None 
            return None

        img = Image.open(BytesIO(result.stdout))
        
        # === 新增：裁剪逻辑 ===
        if crop_box:
            # crop_box 格式 (x1, y1, x2, y2)
            img = img.crop(crop_box)
            
        img.save(path)
        return path
    except Exception as e:
        print(f"【截图异常】{e}")
        return None
# ================= 核心：解析执行多行指令 =================

def execute_multiline_adb(text_block):
    """
    解析用户多行文本并执行
    """
    if not text_block:
        return

    lines = text_block.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue 

        print(f"执行: {line}")

        # 处理 sleep/wait
        parts = line.split()
        if parts[0].lower() in ["sleep", "wait", "timeout"]:
            try:
                time.sleep(float(parts[1]))
            except:
                time.sleep(1)
            continue

        # 处理 adb 指令
        # 移除可能存在的 "adb " 前缀
        if line.startswith("adb "):
            line = line[4:]
            
        cmd_parts = line.split()
        
        # 补全 shell
        adb_args = []
        if cmd_parts[0] == "shell":
            adb_args = cmd_parts
        else:
            adb_args = ["shell"] + cmd_parts

        run_adb_cmd(adb_args)
        time.sleep(0.1) 

# ================= 辅助工具 =================

def adb_click(x, y):
    run_adb_cmd(["shell", "input", "tap", str(x), str(y)])

def adb_swipe(x1, y1, x2, y2, duration=300):
    run_adb_cmd(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

# 简单的图像处理 (复制粘贴自你之前的代码)
def create_white_image_like(input_path: str, output_path: str):
    try:
        img = Image.open(input_path)
        white_img = Image.new("RGB", img.size, (255, 255, 255))
        white_img.save(output_path)
    except: pass

def copy_rectangle_by_ratio(rectangle_ratio, input1_path, input2_path, output_path):
    try:
        img1 = Image.open(input1_path)
        img2 = Image.open(input2_path)
        w, h = img1.size
        l, t, r, b = rectangle_ratio
        region = img1.crop((int(w*l), int(h*t), int(w*r), int(h*b)))
        img2.paste(region, (int(w*l), int(h*t)))
        img2.save(output_path)
    except: pass



# 在文件末尾添加这个辅助函数
def parse_coordinate(coord_str):
    """
    解析 "1273 829" 格式的字符串为 (1273, 829)
    如果解析失败，返回 None
    """
    try:
        parts = coord_str.strip().split()
        if len(parts) >= 2:
            return int(parts[0]), int(parts[1])
    except:
        pass
    return None

# 文件: MyProject/src/adb_utils.py

# ... (保持前面的 imports 和 auto_select_device 等函数不变) ...

def adb_zoom_out(duration=1000):
    """
    [核心技巧] 模拟双指捏合 (缩小/Zoom Out)
    原理：在一条 adb shell 命令中同时执行两个 swipe，利用 & 后台运行
    """
    adb_path = get_adb_path()
    device_id = auto_select_device()
    
    # 假设屏幕分辨率大概是 1600x900 (你可以根据实际情况调整坐标)
    # 手指1: 左上 -> 往中心划
    # 手指2: 右下 -> 往中心划
    
    # 坐标逻辑：(x1, y1) -> (x2, y2)
    finger1 = "input swipe 200 200 700 400 1000"
    finger2 = "input swipe 1400 700 900 500 1000"
    
    # 拼接命令： "input ... & input ..."
    # 注意：必须在一个 adb shell 会话中执行，否则会有延迟，变成分步滑动
    cmd_str = f"{finger1} & {finger2}"
    
    base_cmd = [adb_path]
    if device_id:
        base_cmd.extend(["-s", device_id])
    
    base_cmd.extend(["shell", cmd_str])
    
    print(f"【ADB】执行双指缩放: {cmd_str}")
    try:
        subprocess.run(base_cmd, timeout=5)
    except Exception as e:
        print(f"【缩放失败】{e}")



def stitch_images(img_path_left, img_path_right, output_path, split_x_left=None, split_x_right=None):
    """
    [更新] 拼接两张图片 (支持自定义裁剪 X 轴)
    split_x_left: 左图保留 0 到 split_x_left 的部分
    split_x_right: 右图保留 split_x_right 到 结尾 的部分
    """
    try:
        img1 = Image.open(img_path_left)
        img2 = Image.open(img_path_right)
        w, h = img1.size

        # 1. 处理裁剪坐标 (如果没传，默认保留全图)
        # 左图截止点：默认为图片宽度
        cut_l = int(split_x_left) if split_x_left is not None else w
        # 右图起始点：默认为 0
        cut_r = int(split_x_right) if split_x_right is not None else 0

        # 2. 进行裁剪
        # crop语法: (left, top, right, bottom)
        part1 = img1.crop((0, 0, cut_l, h))
        part2 = img2.crop((cut_r, 0, w, h))

        # 3. 创建画布并拼接
        new_w = part1.width + part2.width
        new_img = Image.new('RGB', (new_w, h))
        
        new_img.paste(part1, (0, 0))
        new_img.paste(part2, (part1.width, 0)) # 紧接着贴在 part1 后面
        
        new_img.save(output_path)
        print(f"【拼图】已生成: {output_path} (左图截至{cut_l}, 右图始于{cut_r})")
        return output_path
    except Exception as e:
        print(f"拼图失败: {e}")
        return None

# 文件: MyProject/src/adb_utils.py

# ... (保持前面的代码不变) ...

# ================= 新增：连续拖拽核心逻辑 (Monkey Script) =================

# 文件: MyProject/src/adb_utils.py

# ... (前面的代码保持不变) ...

# ================= 优化后的连续拖拽逻辑 =================

def run_continuous_drag(point_list, hold_time=1200):
    """
    生成 Monkey 脚本 (慢速丝滑版)
    point_list: [(x1,y1), (x2,y2), ...]
    hold_time: 起始按住的时间(ms)
    """
    if not point_list: return

    # --- 调速参数 (觉得慢可以改小，觉得快可以改大) ---
    STEPS_PER_SEGMENT = 40  # 两点之间插值的数量 (原10 -> 改40)
    STEP_WAIT_MS = 5        # 每移动一小步等待的毫秒数 (新增)

    # Monkey 脚本头
    script_content = "type= user\ncount= 10\nspeed= 1.0\nstart data >>\n"
    
    # 1. 在起点按下
    start_x, start_y = point_list[0]
    script_content += f"DispatchPointer(0, 0, 0, {start_x}, {start_y}, 0, 0, 0, 0, 0, 0, 0)\n"
    
    # 2. 原地等待 (抓取镰刀)
    script_content += f"UserWait({hold_time})\n"
    # 发送一个原地 Move 激活判定
    script_content += f"DispatchPointer(0, 0, 2, {start_x}, {start_y}, 0, 0, 0, 0, 0, 0, 0)\n"

    # 3. 连续移动 (慢速插值)
    for i in range(len(point_list) - 1):
        p1 = point_list[i]
        p2 = point_list[i+1]
        
        # 线性插值
        for step in range(1, STEPS_PER_SEGMENT + 1):
            t = step / STEPS_PER_SEGMENT
            x = int(p1[0] + (p2[0] - p1[0]) * t)
            y = int(p1[1] + (p2[1] - p1[1]) * t)
            
            script_content += f"DispatchPointer(0, 0, 2, {x}, {y}, 0, 0, 0, 0, 0, 0, 0)\n"
            
            # [关键] 增加微小延迟，防止跑太快
            script_content += f"UserWait({STEP_WAIT_MS})\n"
            
    # 4. 抬起
    end_x, end_y = point_list[-1]
    script_content += f"DispatchPointer(0, 0, 1, {end_x}, {end_y}, 0, 0, 0, 0, 0, 0, 0)\n"

    # --- 下面是写入文件和执行逻辑 (保持不变) ---
    local_path = "temp_drag.mks"
    remote_path = "/sdcard/temp_drag.mks"
    
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(script_content)
        
    adb_path = get_adb_path()
    device_id = auto_select_device()
    
    # Push
    cmd_push = [adb_path]
    if device_id: cmd_push.extend(["-s", device_id])
    cmd_push.extend(["push", local_path, remote_path])
    subprocess.run(cmd_push)
    
    # Run
    print(f"【ADB】执行慢速拖拽 (Steps={STEPS_PER_SEGMENT})...")
    cmd_monkey = [adb_path]
    if device_id: cmd_monkey.extend(["-s", device_id])
    cmd_monkey.extend(["shell", "monkey", "-f", remote_path, "1"])
    subprocess.run(cmd_monkey, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try: os.remove(local_path)
    except: pass

# ================= 更新：解析器支持 drag_path =================

def execute_multiline_adb(text_block):
    """
    解析器更新：支持 'drag_path' 指令
    语法: drag_path x1 y1 x2 y2 x3 y3 ...
    """
    if not text_block: return

    lines = text_block.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"): continue
        print(f"执行: {line}")

        parts = line.split()
        cmd = parts[0].lower()

        # === 新增指令: drag_path ===
        if cmd == "drag_path":
            # 解析后面的坐标点
            # 格式: drag_path 100 100 200 200 300 300
            coords = []
            try:
                raw_nums = [int(x) for x in parts[1:]]
                # 两个一组转成 [(x,y), (x,y)]
                coords = list(zip(raw_nums[::2], raw_nums[1::2]))
                if coords:
                    run_continuous_drag(coords)
            except Exception as e:
                print(f"指令解析错误: {e}")
            continue
        
        # ... (下面是之前的 sleep 和 adb shell 逻辑，保持不变) ...
        if cmd in ["sleep", "wait", "timeout"]:
            try: time.sleep(float(parts[1]))
            except: time.sleep(1)
            continue

        if line.startswith("adb "): line = line[4:]
        adb_args = ["shell"] + line.split() if not line.startswith("shell") else line.split()
        run_adb_cmd(adb_args)
        time.sleep(0.1)