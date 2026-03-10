import mss
import mss.tools
import time
import json
import threading
import queue
import os
from src.touchlink import TouchLink

# === 配置区 ===
from config import *
# === 截图写入线程 ===
# 这个队列用来存放待保存的图片数据
save_queue = queue.Queue()

def image_writer_worker():
    """后台线程：专门负责把内存里的图片存到硬盘，不占用打游戏的时间"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
        
    while True:
        # 从队列获取任务
        item = save_queue.get()
        if item is None: # 结束信号
            break
            
        img_data, idx, timestamp = item
        
        # 文件名: 序号_时间戳.png
        filename = os.path.join(SCREENSHOT_DIR, f"act_{idx:04d}_{timestamp}ms.png")
        
        # 保存图片 (IO操作，慢，但这里不影响主线程)
        mss.tools.to_png(img_data.rgb, img_data.size, output=filename)
        
        save_queue.task_done()

# ====================

def wait_for_start(sct):
    print("等待开始信号...")
    while True:
        # 这里用一个小区域监测开始信号
        img = sct.grab({"top": START_SIGNAL_POS[1], "left": START_SIGNAL_POS[0], "width": 1, "height": 1})
        pixel = img.pixel(0, 0)
        dist = abs(pixel[0]-START_SIGNAL_COLOR[0]) + abs(pixel[1]-START_SIGNAL_COLOR[1]) + abs(pixel[2]-START_SIGNAL_COLOR[2])
        if dist < START_TOLERANCE:
            print(">>> 开始回放！ <<<")
            return time.perf_counter_ns()
        time.sleep(0.01)

def play():
    import shutil

    shutil.rmtree("debug_screenshots")
        
    tk = TouchLink()
    
    # 1. 启动截图保存线程
    writer_thread = threading.Thread(target=image_writer_worker, daemon=True)
    writer_thread.start()
    
    # 2. 读取脚本
    # 建议使用刚才量化后的文件
    target_file = "timeline_ai_corrected.json"if os.path.exists("timeline_ai_corrected.json") else "timeline_quantized.json" if os.path.exists("timeline_quantized.json") else "timeline.json"
    with open(target_file, "r", encoding="utf-8") as f:
        actions = json.load(f)
    print(f"已加载 {target_file}，共 {len(actions)} 个动作。")

    with mss.mss() as sct:
        # 预先定义好截图区域，为了调试通常截取整个游戏窗口
        # 这里假设你要截取主显示器，如果只想截取特定区域，请修改这里
        monitor = sct.monitors[1] 
        
        t0 = wait_for_start(sct)
        
        action_idx = 0
        total_actions = len(actions)
        
        try:
            while action_idx < total_actions:
                current_action = actions[action_idx]
                target_ms = current_action["time_ms"] + GLOBAL_OFFSET
                lane = current_action["lane_index"]
                
                now = time.perf_counter_ns()
                elapsed_ms = (now - t0) / 1_000_000
                
                if elapsed_ms >= target_ms:
                    # 1. 执行动作 (Touch)
                    cmd = [{
                        'action': 'swipe', 
                        'args': [PHONE_X[lane], PHONE_Y+2, PHONE_X[lane], PHONE_Y+10], 
                        'duration': 1, 
                        'extras': {'stabilize': 0}
                    }]
                    tk.custom(cmd)
                    
                    # 2. 【关键步骤】立即抓取内存快照 (Grab)
                    # mss.grab 相对较快，将数据丢进队列
                    sct_img = sct.grab(monitor)
                    
                    # 将数据发送给后台线程，不要在这里 to_png
                    save_queue.put((sct_img, action_idx, int(elapsed_ms)))
                    
                    action_idx += 1
                    
                    # 可以在这里打印一下，确认没有卡顿
                    # print(f"Action {action_idx} done.")

        except KeyboardInterrupt:
            print("停止播放。")
        finally:
            print("等待剩余截图保存完成...")
            save_queue.put(None) # 发送结束信号
            writer_thread.join() # 等待后台写完
            print(f"所有截图已保存在 {SCREENSHOT_DIR}/ 目录下。")

if __name__ == "__main__":
    play()