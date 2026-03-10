import os
import json
import re
from src.ai_client import query_vlm

# ================= 配置区 =================

# 【重要】请在这里填入你的智谱AI API Key
os.environ["OPENAI_API_KEY"] = "7659226ea15e41e780cd491f1a65aa99.KdtO7j0JHUBhC6RL" 

# 截图所在的文件夹
SCREENSHOT_DIR = "debug_screenshots"

# 原始谱面文件
INPUT_FILE = "timeline_quantized.json"
# 修正后的输出文件
OUTPUT_FILE = "timeline_ai_corrected.json"

# 量化步长 (每次修正调整多少毫秒)
# 建议设小一点，比如 25 或 50，避免矫枉过正
QUANTIZE_STEP = 150 

# =========================================

def parse_filename(filename):
    """从文件名解析出 list index。例如 act_0005_1234ms.png -> 5"""
    # 正则匹配 act_(\d+)
    match = re.search(r"act_(\d+)_", filename)
    if match:
        return int(match.group(1))
    return None

def main():
    # 1. 读取原始数据
    if not os.path.exists(INPUT_FILE):
        print(f"错误：找不到 {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        actions = json.load(f)
    
    print(f"已加载谱面，共 {len(actions)} 个动作。")
    print("开始 AI 智能修正...")

    # 获取所有截图文件
    if not os.path.exists(SCREENSHOT_DIR):
        print("错误：截图目录不存在")
        return
        
    files = [f for f in os.listdir(SCREENSHOT_DIR) if f.endswith(".png")]
    files.sort() # 按文件名排序

    # 记录修改统计
    stats = {"perfect": 0, "early": 0, "late": 0, "delete": 0, "error": 0}
    
    # 待删除的索引列表
    indices_to_delete = []

    for filename in files:
        idx = parse_filename(filename)
        if idx is None or idx >= len(actions):
            continue
            
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        # === 构造 AI 提示词 ===
        # 这里的提示词非常关键，教 AI 怎么看图
        prompt = """
        请仔细观察这张音游判定瞬间的截图。
        任务是判断点击时机是否准确。请严格按照以下步骤判断，并只返回对应的关键词：

        1. 【第一优先级】看文字：
           - 如果画面中明显出现了橙黄色的汉字 "天籁"，直接回答: PERFECT

        2. 【第二优先级】看位置（如果没有天籁）：
           - 找到横向的判定线（通常有一条细线）。
           - 找到黄色的光圈/圆圈音符。
           - 如果黄色圆圈的主体位于判定线【上方】（说明圆圈还没落下来就截图了，动作太快/太早），回答: EARLY
           - 如果黄色圆圈的主体位于判定线【下方】（说明圆圈已经落过头了才截图，动作太慢/太晚），回答: LATE
           - 如果判定线附近完全没有黄色圆圈（可能是误触），回答: DELETE

        请输出一个单词: PERFECT, EARLY, LATE, 或 DELETE。
        """

        # 调用 AI
        print(f"\n正在分析 [{filename}] (动作序号 {idx})...")
        ai_result = query_vlm(filepath, prompt)
        
        # 清理结果（去掉标点、空格、转大写）
        result = ai_result.strip().upper().replace(".", "")
        
        # === 根据 AI 结果修正数据 ===
        current_action = actions[idx]
        old_time = current_action["time_ms"]
        
        if "PERFECT" in result:
            print(f"  -> [完美] 无需调整。")
            stats["perfect"] += 1
            
        elif "EARLY" in result:
            # 动作太快了(早了) -> 应该晚一点按 -> 时间增加
            new_time = old_time + QUANTIZE_STEP
            actions[idx]["time_ms"] = new_time
            print(f"  -> [太快/EARLY] 圆圈在上方 -> 时间推迟: {old_time} -> {new_time}")
            stats["early"] += 1
            
        elif "LATE" in result:
            # 动作太慢了(晚了) -> 应该早一点按 -> 时间减少
            new_time = old_time - QUANTIZE_STEP
            actions[idx]["time_ms"] = new_time
            print(f"  -> [太慢/LATE] 圆圈在下方 -> 时间提前: {old_time} -> {new_time}")
            stats["late"] += 1
            
        elif "DELETE" in result:
            print(f"  -> [无效/DELETE] 附近无音符 -> 标记删除")
            indices_to_delete.append(idx)
            stats["delete"] += 1
            
        else:
            print(f"  -> [未知响应] AI 回复了: {ai_result}")
            stats["error"] += 1

    # === 执行删除 ===
    # 从后往前删，避免索引偏移，或者直接重构列表
    # 这里使用列表推导式保留未被标记删除的项
    # 注意：actions 是列表，我们需要根据原始 index 来判断
    # 比较稳妥的方法是给要去删的对象打个标
    
    final_actions = []
    for i, act in enumerate(actions):
        if i not in indices_to_delete:
            final_actions.append(act)
    
    # 重新排序（以防修改时间后乱序）
    final_actions.sort(key=lambda x: x["time_ms"])

    # === 保存结果 ===
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_actions, f, indent=4)

    print("\n" + "="*30)
    print("AI 修正完成！")
    print(f"完美 (PERFECT): {stats['perfect']}")
    print(f"太快 (EARLY)  : {stats['early']} (已推迟)")
    print(f"太慢 (LATE)   : {stats['late']} (已提前)")
    print(f"删除 (DELETE) : {stats['delete']}")
    print(f"原始动作数: {len(actions)} -> 修正后: {len(final_actions)}")
    print(f"结果已保存至: {OUTPUT_FILE}")
    print("="*30)

if __name__ == "__main__":
    main()