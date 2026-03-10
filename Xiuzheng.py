import json
import math

# === 配置 ===
INPUT_FILE = "timeline.json"
OUTPUT_FILE = "timeline_quantized.json" # 输出到新文件，防止误操作覆盖
QUANTIZE_STEP = 150  # 量化步长 (ms)

def quantize_and_clean():
    # 1. 读取数据
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            actions = json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到 {INPUT_FILE}")
        return

    if not actions:
        print("数据为空！")
        return

    # 2. 预处理：按时间排序（非常重要，确保第一个音确实是时间最早的）
    actions.sort(key=lambda x: x["time_ms"])

    # 3. 获取基准时间 (t0)
    base_time = actions[0]["time_ms"]
    print(f"基准时间 (第一个音): {base_time}ms")

    processed_actions = []
    seen_notes = set() # 用于去重：格式为 (time, lane)
    
    duplicate_count = 0
    modified_count = 0

    print(">>> 开始量化处理 <<<")

    for action in actions:
        original_time = action["time_ms"]
        lane = action["lane_index"]
        
        # === 核心算法 ===
        # 1. 计算与基准时间的差值
        diff = original_time - base_time
        
        # 2. 将差值四舍五入到最近的 50ms 倍数
        # 例如: diff=48 -> 50, diff=23 -> 0, diff=98 -> 100
        quantized_diff = round(diff / QUANTIZE_STEP) * QUANTIZE_STEP
        
        # 3. 计算新时间
        new_time = int(base_time + quantized_diff)
        
        # 统计变化
        if new_time != original_time:
            modified_count += 1
            
        # === 去重逻辑 ===
        # 检查 "这个时间点" 在 "这条轨道" 是否已经有音符了
        note_identifier = (new_time, lane)
        
        if note_identifier in seen_notes:
            duplicate_count += 1
            # 这是一个重叠音，跳过（不加入结果列表）
            # print(f"  [去重] 移除重叠音: {original_time}ms -> {new_time}ms (轨道 {lane})")
            continue
        
        # 更新时间并保存
        action["time_ms"] = new_time
        processed_actions.append(action)
        seen_notes.add(note_identifier)

    # 4. 再次排序 (以防量化后顺序微调)
    processed_actions.sort(key=lambda x: x["time_ms"])

    # 5. 保存结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_actions, f, indent=4)

    print("-" * 30)
    print(f"处理完成！")
    print(f"原始音符数: {len(actions)}")
    print(f"被微调时间: {modified_count}")
    print(f"去除重复音: {duplicate_count}")
    print(f"剩余音符数: {len(processed_actions)}")
    print(f"结果已保存至: {OUTPUT_FILE}")
    print("-" * 30)
    print("建议将 config.py 或 Player.py 中的文件名改为 timeline_quantized.json 进行测试")

if __name__ == "__main__":
    quantize_and_clean()