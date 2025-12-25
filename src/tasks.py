# 文件: MyProject/src/tasks.py
import time
import os
import ast
from src.ai_client import query_vlm 
# 务必引入 execute_multiline_adb 用于执行 area_adb
from src.adb_utils import adb_click, adb_swipe, adb_zoom_out, parse_coordinate, execute_multiline_adb
from src.adb_utils import stitch_images, execute_multiline_adb, adb_screenshot # 引入新工具

# === 基类：定义标准流程 ===
class GameScriptBase:
    def __init__(self, config):
        self.params = config

        self.s_delay = float(os.environ.get("small_delay", 1.5))
        self.b_delay = float(os.environ.get("big_delay", 8.0))
    def log(self, msg):
        print(f"[{self.__class__.__name__}] {msg}")

    # 1. 复位逻辑 (保持不变)
    def reset_state(self):
        """
        [固定状态复位]
        """
        self.log(">>> [Step 1] 执行复位逻辑...")

        # 侧滑唤醒
        self.log("动作: 侧滑唤醒UI")
        adb_swipe(600, 500, 800, 500, 300) 
        time.sleep(self.s_delay)


        # 点击订单图标
        pos_order = parse_coordinate(os.environ.get("reset_pos_order"))
        if pos_order:
            self.log(f"动作: 点击订单 {pos_order}")
            adb_click(pos_order[0], pos_order[1])
        time.sleep(self.s_delay)

        # 缩放
        self.log("动作: 双指缩放")
        adb_zoom_out() 
        time.sleep(self.s_delay + 1.0)

        # 退出订单
        pos_exit_order = parse_coordinate(os.environ.get("reset_pos_exit_order"))
        if pos_exit_order:
            self.log(f"动作: 退出订单 {pos_exit_order}")
            adb_click(pos_exit_order[0], pos_exit_order[1])
        time.sleep(self.s_delay)

        # 点击蒲公英
        pos_dandelion = parse_coordinate(os.environ.get("reset_pos_dandelion"))
        if pos_dandelion:
            self.log(f"动作: 点击蒲公英 {pos_dandelion}")
            adb_click(pos_dandelion[0], pos_dandelion[1])
        time.sleep(self.b_delay)

        # 退出蒲公英
        pos_exit_dandelion = parse_coordinate(os.environ.get("reset_pos_exit_dandelion"))
        if pos_exit_dandelion:
            self.log(f"动作: 退出蒲公英 {pos_exit_dandelion}")
            adb_click(pos_exit_dandelion[0], pos_exit_dandelion[1])
        time.sleep(self.s_delay)

    # 2. 定位逻辑 (从 execute 中提取出来)
    def navigate_to_target(self):
        """
        [进场] 执行 '区域选中ADB'
        """
        self.log(">>> [Step 2] 定位目标区域...")
        area_cmd = self.params.get("area_adb")
        if area_cmd:
            execute_multiline_adb(area_cmd)
        else:
            self.log("提示: 当前任务无需定位或未配置 area_adb")
        
        # 进场后通常需要一点等待，让二级菜单弹出来
        time.sleep(self.s_delay)

    # 4. 退出界面逻辑 (新增)
    def exit_interface(self):

        """
        [退场] 
        """
        self.log(">>> [Step 2] 定位目标区域...")
        area_cmd = self.params.get("quit_adb")
        if area_cmd:
            execute_multiline_adb(area_cmd)
        else:
            self.log("提示: 当前任务无需定位或未配置 quit_adb")
        
        # 进场后通常需要一点等待，让二级菜单弹出来
        time.sleep(self.s_delay)

    # === 核心流程控制 ===
    def run(self):
        self.log("====== 任务序列启动 ======")
        
        # 调试断点 (默认注释掉，需要调试时打开)
        # 1. 复位 (Reset)
        self.reset_state()

        # 2. 定位 (Locate)
        self.navigate_to_target()
        
        # 3. 运行 (Execute)
        self.log(">>> [Step 3] 执行核心逻辑...")
        try:
            self.execute()
        except Exception as e:
            self.log(f"ERROR: 执行出错: {e}")
            
        # 4. 退出 (Exit)
        self.exit_interface()
        
        self.log("====== 任务序列结束 ======\n")

    def execute(self):
        raise NotImplementedError

    def parse_list(self, param_key):
        raw = self.params.get(param_key, "[]")
        try:
            return ast.literal_eval(raw)
        except:
            self.log(f"参数 {param_key} 格式错误")
            return []

# ==========================================
# 任务定义区
# ==========================================
# 文件: MyProject/src/tasks.py

# ... (前面的 imports 和 GameScriptBase 保持不变) ...

class FarmingTask(GameScriptBase):
    LABEL = "1. 种田 (智能版)"
    PARAM_CONFIG = {
        # === 基础定位 ===
        "area_adb": {
            "label": "区域选中ADB (定位到田地附近)",
            "type": "text",
            "default": "input tap 1115 227\nsleep 1"
        },
        "field_select_adb": {
            "label": "选中田地ADB (点击田地弹出作物栏)",
            "type": "text",
            "default": "input tap 803 464\nsleep 1"
        },
        "farm_info_pos": {
            "label": "农田说明图标坐标 (x y) - 用于复位作物栏",
            "type": "string",
            "default": "168 772"
        },
        "close_seed_bar_adb": {
            "label": "无需播种时关闭动作 (通常点击空地)",
            "type": "text",
            # 默认点击屏幕上方空白处，通常能关闭底部栏
            "default": "sleep 1\ninput tap 300 300\nsleep 1" 
        },
        # === 核心：AI 提示词增强 ===
        "crop_prompt_names": {
            "label": "作物名称提示 (用于辅助AI识别顺序，用逗号分隔)",
            "type": "text",
            # 这里填你希望告诉 AI 的顺序
            "default": "小麦，大豆，甘蔗，水稻，白菜，辣椒，土豆，苎麻, 棉花, 南瓜, 红薯" 
        },
        # === 动作轨迹配置 ===
        "sickle_pos": {
            "label": "镰刀位置 (x y)",
            "type": "string",
            "default": "795 770"
        },
        "field_path": {
            "label": "通用田地划过轨迹 (纯坐标串)",
            "type": "text",
            # 这就是之前算好的 6x6 网格 S型扫描路径
            "default": "799 465 1144 318 1208 348 867 491 935 517 1260 367 1317 391 1003 544 1071 569 1400 416 1500 443 1143 601 1043 601"
        },
        
        # === 作物配置 (11种) ===
        "crop_limits": {
            "label": "作物库存上限列表",
            "type": "string",
            # 11个50
            "default": "[50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]" 
        },
        "crop_pos_list": {
            "label": "作物种子位置列表 ['x y', ...]",
            "type": "string",
            # 前7个是左页，后4个是右页，Y固定为760
            "default": "['340 760', '475 760', '610 760', '745 760', '880 760', '1015 760', '1150 760', '845 760', '980 760', '1115 760', '1250 760']"
        },
        "crop_is_right_side": {
            "label": "作物是否在右侧页 (0=左, 1=右)",
            "type": "string",
            # 前7个为0，后4个为1
            "default": "[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]"
        },
        "crop_bar_swipe_adb": {
            "label": "作物栏翻页动作 (向左滑)",
            "type": "text",
            # 稍微滑长一点确保翻过去
            "default": "input swipe 1000 760 300 760 600"
        },
        
        # === 拼图识别 ===
        "stitch_left_x": { "label": "拼图: 左图保留宽度 (X)", "type": "int", "default": "1230" },
        "stitch_right_x": { "label": "拼图: 右图起始位置 (X)", "type": "int", "default": "780" }
    }

    def execute(self):
        # 1. 点击田地
        
        # 2. 状态判断 
        screenshot_path = "farm_state.png"
        adb_screenshot(screenshot_path)
        
        check_prompt = """
        请分析这张游戏截图，判断当前处于什么状态。
        只返回一个关键词：
        - "harvest" : 画面底部有镰刀图标。
        - "plant" : 画面底部有作物种子选择栏。
        - "wait" : 其他情况。
        """
        state = query_vlm(screenshot_path, check_prompt)
        self.log(f"AI判断状态: {state}")

        if "harvest" in state:
            self.do_harvest()
            time.sleep(self.s_delay)
            self.do_plant_logic() # 收完直接种
            
        elif "plant" in state:
            self.do_plant_logic()
            
        else:
            self.log("无需操作")

    def do_harvest(self):
        self.log(">>> 执行收获逻辑")
        
        sickle = self.params.get("sickle_pos", "795 770").strip()
        path = self.params.get("field_path", "").strip()
        
        # 拼装命令：drag_path 镰刀点 轨迹点
        full_cmd = f"drag_path {sickle} {path}\nsleep 1"
        
        self.log(f"生成收割指令: {full_cmd[:50]}...")
        execute_multiline_adb(full_cmd)
        self.log("收获完成")

    def do_plant_logic(self):
        self.log(">>> 执行播种逻辑")
        
        info_pos = self.params.get("farm_info_pos", "168 772")
        info_coords = parse_coordinate(info_pos)
        execute_multiline_adb(self.params.get("field_select_adb"))
        time.sleep(self.s_delay) # 等作物栏弹出来

        # ==========================================
        # 步骤 2: 截图识别库存
        # ==========================================
        # 左图
        img_left = "crop_bar_1.png"
        adb_screenshot(img_left)
        
        # 翻页
        execute_multiline_adb(self.params.get("crop_bar_swipe_adb"))
        time.sleep(self.s_delay)
        
        # 右图
        img_right = "crop_bar_2.png"
        adb_screenshot(img_right)
        
        # 拼图
        img_stitched = "crop_bar_full.png"
        split_l = int(self.params.get("stitch_left_x", 1600))
        split_r = int(self.params.get("stitch_right_x", 0))
        stitch_images(img_left, img_right, img_stitched, split_l, split_r)
        
        # AI 识别        
        crop_names_str = self.params.get("crop_prompt_names", "")
        # 2. 构造 Prompt，使用 f-string {crop_names_str} 插入变量
        count_prompt = f"请读取底部作物栏的库存数字，依次是[{crop_names_str}]，返回纯数字列表: [x, x, ...]"        
        ai_res = query_vlm(img_stitched, count_prompt)
        self.log(f"AI读取库存: {ai_res}")
        
        # ==========================================
        # 步骤 3: 决策与播种
        # ==========================================
        try:
            import re
            nums = re.findall(r'\d+', ai_res)
            current_counts = [int(n) for n in nums]
            
            limits = self.parse_list("crop_limits")
            # 这里获取的是坐标字符串列表 ['200 850', '350 850'...]
            seed_pos_list = self.parse_list("crop_pos_list") 
            is_right_list = self.parse_list("crop_is_right_side")
            
            # 安全检查
            if not current_counts: return

            target_index = -1
            min_count = 99999
            
            loop_len = min(len(current_counts), len(limits), len(seed_pos_list))
            
            for i in range(loop_len):
                curr = current_counts[i]
                limit = limits[i]
                if curr < limit and curr < min_count:
                    min_count = curr
                    target_index = i
            
            if target_index != -1:
                self.log(f"决定种植第 {target_index+1} 种作物 (库存 {min_count})")
                
                # --- 核心：准备播种 ---
                
                # 3.1 再次归零 (为了确保位置准确)
                # 因为刚才翻页去截图了，现在界面在第二页，如果目标在第一页，需要复位
                # 如果目标就在第二页，其实不用复位，但为了逻辑简单，建议统一复位再操作
                # 或者：判断 target_index 是否在右侧，如果刚才截图完在右侧，且目标也在右侧，就不动
                # 这里为了稳妥，采用最笨的办法：复位 -> 再根据需要翻页
                
                # 这里我们简化一下：刚才截图完停在“右页”。
                # 如果目标是左页(0)，需要复位。
                # 如果目标是右页(1)，不需要动 (假设翻页后就在右页)。
                
                target_is_right = 0
                if target_index < len(is_right_list):
                    target_is_right = is_right_list[target_index]
                
                if target_is_right == 0:
                    self.log("目标在左侧，执行复位...")
                    # 点击说明 -> 点击田地
                    if info_coords: adb_click(info_coords[0], info_coords[1])
                    time.sleep(self.s_delay)
                    execute_multiline_adb(self.params.get("field_select_adb"))
                    time.sleep(self.s_delay)
                else:
                    self.log("目标在右侧，保持当前页面")
                    # 如果刚才截图后你没有复位，那现在就在右侧，直接操作即可
                
                # 3.2 提取种子坐标
                # 列表里可能是 "input tap 200 850" 或者 "200 850"，我们需要清洗出纯坐标
                raw_pos = seed_pos_list[target_index]
                # 简单清洗：去掉非数字字符，只留空格和数字
                clean_pos = re.sub(r'[^\d\s]', '', raw_pos).strip() 
                
                # 3.3 拼装播种指令
                path = self.params.get("field_path", "").strip()
                plant_cmd = f"drag_path {clean_pos} {path}\nsleep 1"
                
                self.log(f"生成播种指令: {plant_cmd}...")
                execute_multiline_adb(plant_cmd)
                
            else:
                self.log("库存充足")
                # === 关键修改：执行关闭动作 ===
                execute_multiline_adb(self.params.get("close_seed_bar_adb"))

        except Exception as e:
            self.log(f"决策出错: {e}")
class GatheringTask(GameScriptBase):
    LABEL = "2. 采集 (全自动版)"
    
    PARAM_CONFIG = {
        # === 基础操作 ===
        "area_adb": {
            "label": "区域选中ADB",
            "type": "text",
            "default": "input swipe 800 450 100 800 5000\ninput tap 1314 460\nsleep 1"
        },
        "btn_pos": {
            "label": "收获/开始生产按键ADB",
            "type": "text",
            "default": "input tap 1243 750"
        },
        "nav_adb": {
            "label": "地点切换ADB",
            "type": "text", 
            "default": "input tap 823 662"
        },
        "quit_adb": {
            "label": "退出界面ADB",
            "type": "text", 
            "default": "input tap 763 798"
        },
        "location_count": {
            "label": "林地数量 (整数)",
            "type": "int",
            "default": "3"
        },

        # === 核心基础配置：4个物理格子坐标 ===
        "slot_adbs": {
            "label": "顶部4个格子的固定ADB (物理坐标)",
            "type": "text",
            # 定义好这4个位置，后面代码会自动按顺序取用
            "default": "['input tap 1040 206', 'input tap 1160 206', 'input tap 1280 206', 'input tap 1400 206']"
        },

        # === 新增：截图裁剪配置 ===
        "digit_crop_box": {
            "label": "库存数字截图裁剪区域 [x1, y1, x2, y2]",
            "type": "string", # string 类型也就是单行文本框
            "default": "[1060, 394, 1160, 464]"
        },
        # === 业务配置 ===
        "item_names_list": {
            "label": "各林地作物名称 [['松木'], ['竹子']...]",
            "type": "text",
            # 只要填了名字，代码会自动去点对应顺序的格子
            "default": "[['木材'], ['青竹'], ['原始土','矿料']]"
        },
        
        # 移除了 item_slot_indices_list，由代码自动推导
        
        "item_limits_list": {
            "label": "物品库存上限 [[100], [100]...]",
            "type": "text",
            "default": "[[100], [100], [100, 100]]"
        }
    }

    def execute(self):
        count = int(self.params.get("location_count", 1))
        nav = self.params.get("nav_adb").strip()
        
        # 1. 解析全局格子配置
        master_slots = self.parse_list("slot_adbs")
        
        # 2. 解析业务数据
        names_group = self.parse_list("item_names_list")
        limits_group = self.parse_list("item_limits_list")
        
        for i in range(count):
            self.log(f"--- 正在处理第 {i+1}/{count} 个林地 ---")
            
            # 获取当前林地的数据
            curr_names = names_group[i] if i < len(names_group) else []
            curr_limits = limits_group[i] if i < len(limits_group) else []
            
            # === 核心逻辑优化：自动生成 ADB 指令 ===
            curr_select_cmds = []
            
            # 根据当前地点有几个物品 (len(curr_names))，就取前几个格子
            # 例如：有2个物品，就取 master_slots[0] 和 master_slots[1]
            for idx in range(len(curr_names)):
                if idx < len(master_slots):
                    curr_select_cmds.append(master_slots[idx])
                else:
                    self.log(f"警告：物品数量({len(curr_names)}) 超过了配置的格子数({len(master_slots)})")
                    # 超过部分无法点击，或者你可以填一个默认值

            if curr_names:
                self.process_single_location(curr_names, curr_select_cmds, curr_limits)
            else:
                self.log("未配置该地点的物品，跳过")
            
            time.sleep(self.s_delay)
            
            # 切换地点
            if i < count - 1:
                execute_multiline_adb(nav)
                

    def process_single_location(self, names, selects, limits):
        """处理单个地点的核心逻辑"""
        screenshot_path = "gather_state.png"
        adb_screenshot(screenshot_path)
        
        check_prompt = "判断右下角按钮，从以下选择三选一：'收获'、'开始生产' 或 '加速' (工作中)。只回关键词。"
        state = query_vlm(screenshot_path, check_prompt)
        self.log(f"当前状态: {state}")

        if "harvest" in state or "收获" in state:
            self.do_harvest()
            time.sleep(self.s_delay)
            self.do_production_logic(names, selects, limits)
            
        elif "plant" in state or "生产" in state:
            self.do_production_logic(names, selects, limits)
            
        elif "working" in state or "加速" in state:
            self.log("正在工作中，跳过")
        else:
            self.log("未知状态，跳过")

    def do_harvest(self):
        self.log(">>> 执行收获")
        cmd = self.params.get("btn_pos")
        execute_multiline_adb(cmd)

    def do_production_logic(self, names, selects, limits):
        self.log(">>> 轮询库存...")
        
        current_counts = []
        # 安全检查
        loop_len = min(len(names), len(selects))
        crop_list = self.parse_list("digit_crop_box")
        crop_box = tuple(crop_list) if len(crop_list) == 4 else None
        if crop_box is None:
            self.log("警告：裁剪参数格式错误，将使用全图识别")
        for k in range(loop_len):
            item_name = names[k]
            select_cmd = selects[k]
            
            # 1. 选中
            execute_multiline_adb(select_cmd)
            time.sleep(self.s_delay)
            
            # 2. 截图
            img_name = f"item_{k}.png"
            adb_screenshot(img_name, crop_box=crop_box)
            
            # 提示词：读取中间显示的库存
            prompt = (
                f"这是'{item_name}'的库存数字特写。请识别图中的纯数字整数。"
                f"【重要规则】图片中只有数字，**绝对没有英文字母**！"
                f"如果你看到圆圈形状（如 'o', 'O'），请务必将其识别为数字 '0'。"
                f"如果存在斜杠 '/' 及其后面的数字（如 '54/1'），请忽略斜杠部分，只读前面的库存数。"
            )
            
            ai_res = query_vlm(img_name, prompt)
                        # === 新增：暴力清洗数据，把 o/O 变回 0 ===
            ai_res = ai_res.replace('o', '0').replace('O', '0')
            try:
                import re
                nums = re.findall(r'\d+', ai_res)
                count = int(nums[0]) if nums else 9999
            except:
                count = 9999
            
            self.log(f"[{item_name}] 库存: {count}")
            current_counts.append(count)

        # 决策
        if not current_counts: return

        target_index = -1
        min_count = 99999
        
        # 安全检查
        decision_len = min(len(current_counts), len(limits))
        
        for i in range(decision_len):
            curr = current_counts[i]
            limit = limits[i]
            if curr < limit and curr < min_count:
                min_count = curr
                target_index = i
        
        if target_index != -1:
            target_name = names[target_index]
            self.log(f"决定生产: {target_name}")
            
            # 1. 再次选中
            execute_multiline_adb(selects[target_index])
            time.sleep(self.s_delay)
            
            # 2. 生产
            btn_cmd = self.params.get("btn_pos")
            execute_multiline_adb(btn_cmd)
        else:
            self.log("库存充足，不生产")
class ProcessingTask(GameScriptBase):
    LABEL = "3. 加工 (普通/特殊工坊)"
    
    PARAM_CONFIG = {
        # === 基础导航 ===
        "area_adb": {
            "label": "区域选中ADB (进入起始位置)",
            "type": "text",
            "default": "input tap 1223 760\nsleep 2"
        },
        "nav_adb": {
            "label": "切换上一个工坊ADB (向左切换),开头先切换一次。注意下面的参数顺序是执行顺序",
            "type": "text", 
            "default": "input tap 110 664"
        },
        "quit_adb": {
            "label": "退出界面ADB",
            "type": "text", 
            "default": "input tap 100 100"
        },
        "location_count": {
            "label": "工坊总数量",
            "type": "int",
            "default": "27"
        },
        "ui_types": { 
            "label": "UI类型 (0=普通, 1=特殊)", 
            "type": "string", 
            # 你的实际配置
            "default": "[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]" 
        },

        # === [Type 0] 普通工坊配置 ===
        "normal_slot_adbs": {
            "label": "Type0: 右上角8个原料格物理坐标",
            "type": "text",
            # 这里填右上角那两排格子的坐标
            "default": "['input tap 1050 220', 'input tap 1160 220', 'input tap 1260 220', 'input tap 1360 220', 'input tap 1050 320', 'input tap 1160 320', 'input tap 1260 320', 'input tap 1360 320']"
        },
        "normal_harvest_adb": {
            "label": "Type0: 收获动作 (点击下方6个生产位)",
            "type": "text",
            # 依次点击下方的6个圆盘/格子
            "default": "input tap 840 815\nsleep 1\ninput tap 1165 550\nsleep 1\ninput tap 710 815\nsleep 1\ninput tap 1165 550\nsleep 1\ninput tap 587 815\nsleep 1\ninput tap 1165 550\nsleep 1\ninput tap 463 815\nsleep 1\ninput tap 1165 550\nsleep 1\ninput tap 331 815\nsleep 1\ninput tap 1165 550\nsleep 1\ninput tap 223 815\nsleep 1\ninput tap 1165 550\nsleep 1\n"
        },
        "normal_produce_btn": {
            "label": "Type0: 开始制作按钮",
            "type": "text",
            "default": "input tap 1300 760"
        },
        # === 新增：Type 0 截图裁剪配置 ===
        "normal_digit_crop_box": {
            "label": "Type0: 库存数字截图裁剪区域 [x1, y1, x2, y2]",
            "type": "string",
            "default": "[1035, 530, 1135, 600]"
        },

        # === [Type 1] 特殊工坊配置 ===
        "special_harvest_btn": {
            "label": "Type1: 收获按钮 (捡蛋/收蜜)",
            "type": "text",
            "default": "input tap 1314 733\nsleep 1\ninput tap 1314 667"
        },
        "special_feed_btn": {
            "label": "Type1: 喂食/添加按钮",
            "type": "text",
            "default": "input tap 1080 733"
        },

        # === 物品配置 (平行列表) ===
        "item_names_list": {
            "label": "产品名称列表 [['粉1','粉2'], ['膏1']...]",
            "type": "text",
            "default": "[['元气壮骨粉','益寿延珍粉','畅悦清润粉'], ['白玉萤肌膏','逐元润颜膏','玲珑泽面膏'],['贝壳粉','珍珠粉','藕粉'], ['无芯莲','裙边干','甲鱼壳'],['青染布','红染布','紫染布','黄染布'],['青染料','红染料','紫染料','黄染料'],['烤地瓜','烤土豆','烤豆腐','烤鸡翅','烤羊腿'], ['布娃娃','虎头帽','荷包','绣球'],['麻布','绒线','棉布','蚕丝线'],['南瓜籽','粉丝','干豆豉'],['砚','笔','纸'],['陶器','单色瓷','彩绘瓷'],['陶土','釉料','釉彩'],['竹蜻蜓','泥哨','竹板','陀螺'],['竹片','竹篓','麻绳','斗笠'],['糯米糕','鸡蛋糕','发糕','南瓜糕','马蹄糕'],['陶艺木具','榫卯','鲁班锁'],['油豆腐','腐竹','豆腐乳','豆筋','豆腐脑','豆腐干'],['咸鸡蛋','酸菜','腌鸡肉','腌土豆','腌羊肉'],['鸡蛋饼','烧饼','蔬菜饼','土豆饼','南瓜饼','地瓜饼'],['糖','红糖','麦糖'],['鸡饲料','羊饲料','蚕食'],['豆腐','豆浆','豆豉'],['面粉','糕粉','土豆粉','地瓜粉'],['蚕丝'],['羊毛','羊肉'],['鸡蛋','鸡肉']]" 
        },
        "item_limits_list": {
            "label": "产品库存上限",
            "type": "text",
            "default":  "[[50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50, 50], [50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50], [50, 50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50, 50], [50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50], [50, 50, 50, 50, 50, 50], [50, 50, 50, 50, 50], [50, 50, 50, 50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50], [50, 50, 50, 50], [50], [50, 50], [50, 50]]"
        }
    }


    def execute(self):

        # 2. 准备循环数据
        count = int(self.params.get("location_count", 27))
        nav_cmd = self.params.get("nav_adb").strip()
        
        ui_types = self.parse_list("ui_types")
        names_group = self.parse_list("item_names_list")
        limits_group = self.parse_list("item_limits_list")
        
        # 预加载物理坐标
        normal_slots = self.parse_list("normal_slot_adbs")

        # 3. 开始倒序/正序循环 (根据你的 nav 是向前还是向后，这里按你的逻辑是向左切)
        for i in range(count):
            self.log(f"--- 处理第 {i+1}/{count} 个工坊 ---")
            
            # 导航逻辑：除了第一次进入不用切，后面都要切
            # 或者按照你的逻辑：area_adb 进的是第27个? 还是 dummy?
            # 你的代码写的是：先 nav，再处理。这意味着 area_adb 进去的位置是 "起点"，然后立刻左切进入 "第一个待处理"。
            # 我们保持你的逻辑：
            self.log("动作: 切换工坊")
            execute_multiline_adb(nav_cmd)
            time.sleep(self.s_delay) 
            
            # 获取数据
            curr_type = ui_types[i] if i < len(ui_types) else 0
            curr_names = names_group[i] if i < len(names_group) else []
            curr_limits = limits_group[i] if i < len(limits_group) else []

            if not curr_names:
                self.log("未配置物品，跳过")
                continue

            # 分发逻辑
            if curr_type == 0:
                self.process_normal_factory(curr_names, curr_limits, normal_slots)
            else:
                self.process_special_factory(curr_names, curr_limits)


    def process_normal_factory(self, names, limits, slot_adbs):
        """
        [Type 0] 养生坊/药膏坊逻辑
        """
        # 1. 先收获 (盲点下方6个位置)
        self.log("执行收获...")
        execute_multiline_adb(self.params.get("normal_harvest_adb"))
        time.sleep(self.s_delay)

        # 2. 轮询读取当前库存
        self.log("读取库存...")
        current_counts = []
        
        # 安全检查
        item_count = min(len(names), len(slot_adbs))
        # === 修改点：从参数读取裁剪区域 ===
        crop_list = self.parse_list("normal_digit_crop_box")
        crop_box = tuple(crop_list) if len(crop_list) == 4 else None
        

        for k in range(item_count):
            # 点击右上角对应的格子
            execute_multiline_adb(slot_adbs[k])
            time.sleep(self.s_delay)
            
            # 截图并识别
            img_name = f"factory_item_{k}.png"
            adb_screenshot(img_name, crop_box=crop_box)
            
            # 提示词：读取中间显示的库存
            prompt = (
                f"这是'{names[k]}'的库存数字特写。请识别图中的纯数字整数。"
                f"【重要规则】图片中只有数字，**绝对没有英文字母**！"
                f"如果你看到圆圈形状（如 'o', 'O'），请务必将其识别为数字 '0'。"
                f"如果存在斜杠 '/' 及其后面的数字（如 '54/1'），请忽略斜杠部分，只读前面的库存数。"
            )
            res = query_vlm(img_name, prompt)
                        # === 新增：暴力清洗数据，把 o/O 变回 0 ===
            res = res.replace('o', '0').replace('O', '0')
            
            try:
                import re
                nums = re.findall(r'\d+', res)
                val = int(nums[0]) if nums else 9999
            except:
                val = 9999
            
            self.log(f"[{names[k]}] 库存: {val}")
            current_counts.append(val)

        # 3. 生产循环 (假设有6个生产位，就尝试填满6次)
        # 贪心算法：每次都生产最缺的那个，并模拟库存+1
        
        produce_btn = self.params.get("normal_produce_btn")
        
        for slot_idx in range(6): # 6个生产坑位
            target_idx = -1
            min_val = 99999
            
            # 找最缺的
            for k in range(min(len(current_counts), len(limits))):
                curr = current_counts[k]
                limit = limits[k]
                
                if curr < limit and curr < min_val:
                    min_val = curr
                    target_idx = k
            
            if target_idx != -1:
                item_name = names[target_idx]
                self.log(f"生产位[{slot_idx+1}/6]: 制作 {item_name} (模拟库存 {min_val}->{min_val+1})")
                
                # 再次点击选中 (防止焦点丢失)
                execute_multiline_adb(slot_adbs[target_idx])
                time.sleep(self.s_delay)
                
                # 点击制作
                execute_multiline_adb(produce_btn)
                time.sleep(self.s_delay)
                
                # === 关键：手动增加计数，影响下一次循环决策 ===
                current_counts[target_idx] += 1
            else:
                self.log(f"生产位[{slot_idx+1}/6]: 无需生产")
                break # 如果都不缺，直接退出循环
    def process_special_factory(self,   names,limits):
        """
        [Type 1] 鸡舍/羊圈逻辑
        图2显示：右下角有两个资源 (比如 鸡蛋:20, 鸡肉:0)
        """
        # 1. 先收获
        self.log("执行捡蛋/收货...")
        execute_multiline_adb(self.params.get("special_harvest_btn"))
        time.sleep(self.s_delay) # 等动画
        
        # 2. 截图读取右下角资源
        img_name = "special_factory.png"
        adb_screenshot(img_name)
        
        # 提示词优化：针对图2右下角
        prompt = f"请读取图片右下角'拥有：'后面的({str(names)}物品的)数字列表。例如'拥有：鸡蛋 20 鸡肉 0'，请返回 [20, 0]。"
        res = query_vlm(img_name, prompt)
        self.log(f"AI读取资源: {res}")
        
        try:
            import re
            nums = re.findall(r'\d+', res)
            # 假设拥有列表顺序和 limits 顺序一致
            current_owned = [int(n) for n in nums]
            
            should_feed = False
            # 逻辑：只要有任意一个资源低于上限，就喂食？或者必须两个都低？
            # 通常逻辑是：只要缺货，就得喂。
            for k in range(min(len(current_owned), len(limits))):
                if current_owned[k] < limits[k]:
                    should_feed = True
                    self.log(f"资源[{k}] {current_owned[k]} < {limits[k]}，需要喂食")
            
            if should_feed:
                self.log("执行喂食...")
                execute_multiline_adb(self.params.get("special_feed_btn"))
            else:
                self.log("资源充足，不喂食")
                
        except Exception as e:
            self.log(f"特殊工坊识别出错: {e}")
class CookingTask(GameScriptBase):
    LABEL = "4. 做菜(固定位置/盲盒模式)"
    
    PARAM_CONFIG = {
            # === 基础操作 ===
            "area_adb": {
                "label": "进入厨房 (★运行前请确保：所有菜谱分类处于折叠状态★)",
                "type": "text",
                "default": "input tap 875 122\nsleep 8"
            },
            "cook_btn_adb": {
                "label": "开始/快速烹饪按钮ADB,包括等待动画",
                "type": "text",
                "default": "input tap 1256 770\nsleep 5\ninput tap 1256 770\n"
            },
            "quit_adb": {
                "label": "退出界面ADB",
                "type": "text", 
                "default": "input tap 1486 45\nsleep 5"
            },

            # === 统一参数 ===
            "cook_batch_count": {
                "label": "单次制作次数 (缺货时连点多少下)",
                "type": "int",
                "default": "1"
            },
            
            # === 核心配置：位置遍历 ===
            "position_adbs_list": {
                "label": "位置遍历列表 ADB (依次点击屏幕上的格子)",
                "type": "text",
                "default": "['input tap 1160 203\\nsleep 1\\ninput tap 1160 300\\nsleep 1', 'input tap 1160 203\\nsleep 1\\ninput tap 1160 406\\nsleep 1',  'input tap 1160 203\\nsleep 1\\ninput tap 1160 525\\nsleep 1',  'input tap 1160 203\\nsleep 1\\ninput tap 1160 656\\nsleep 1' ]",
                "help": "请填入点击不同菜品位置的指令。脚本将按顺序执行。"
            },
            
            "dish_reset_adbs_list": {
                "label": "位置复位列表 ADB (做完该位置的菜后，如何返回/关闭弹窗)",
                "type": "text",
                # 注意：下面这行末尾改成了逗号
                "default": "['input swipe 1210 200 1210 880 2000\\nsleep 1\\ninput tap 1160 186\\nsleep 1','input swipe 1210 200 1210 880 2000\\nsleep 1\\ninput tap 1160 186\\nsleep 1','input swipe 1210 200 1210 880 2000\\nsleep 1\\ninput tap 1160 186\\nsleep 1','input swipe 1210 200 1210 880 2000\\nsleep 1\\ninput tap 1160 186\\nsleep 1']",
                "help": "重要：做完菜后通常需要关闭详情页或弹窗，才能点击下一个位置。请确保此列表长度与位置列表一致。"
            }
        }

    def execute(self):
        # 1. 解析参数
        pos_adbs = self.parse_list("position_adbs_list")
        reset_adbs = self.parse_list("dish_reset_adbs_list")
        
        cook_btn = self.params.get("cook_btn_adb")
        batch_count = int(self.params.get("cook_batch_count", 1))
        
        # 3. 循环遍历
        # 以位置列表长度为准
        total_steps = len(pos_adbs)
        if total_steps == 0:
            self.log("未配置位置列表，任务结束")
            return

        self.log(f"开始任务：共遍历 {total_steps} 个位置，单次制作 {batch_count} 份")

        for i in range(total_steps):
            # 获取当前步骤的指令
            curr_pos_cmd = pos_adbs[i]
            # 获取对应的复位指令，防止索引越界
            curr_reset_cmd = reset_adbs[i] if i < len(reset_adbs) else ""
            
            self.log(f"--- 步骤 [{i+1}/{total_steps}] ---")
            
            # 3.1 选中位置
            self.log(f"执行位置选中...")
            execute_multiline_adb(curr_pos_cmd)
            time.sleep(self.s_delay)
            
            # 3.2 盲做
            self.log(f"执行烹饪 ({batch_count}次)...")
            for k in range(batch_count):
                execute_multiline_adb(cook_btn)
                # 如果 cook_btn 里面包含等待动画的时间，这里 sleep 可以短一点，否则建议给足时间
                time.sleep(self.s_delay) 

            # 3.3 复位 (关键步骤)
            if curr_reset_cmd:
                self.log(f"执行复位/收尾...")
                execute_multiline_adb(curr_reset_cmd)
                time.sleep(self.s_delay)
            else:
                self.log("警告：该位置未配置复位指令，可能影响后续操作")

class OrderTask(GameScriptBase):
    LABEL = "5. 订单 (自动交付)"
    
    PARAM_CONFIG = {
        # === 进场 ===
        "area_adb": {
            "label": "区域选中ADB (点击主界面订单图标)",
            "type": "text",
            # 使用你之前提供的 reset_pos_order 坐标
            "default": "input tap 1273 829\nsleep 2"
        },
        
        # === 业务逻辑 ===
        "slot_select_adbs": {
            "label": "订单栏位选中ADB列表 (从左到右依次点击)",
            "type": "text",
            # 根据截图估算的5个栏位坐标，你可以根据实际情况调整
            "default": "['input tap 285 430','input tap 405 430','input tap 530 430','input tap 660 430','input tap 780 430','input tap 900 430','input tap 1020 430','input tap 1140 430','input tap 1260 430','input tap 1380 430']"
        },
        "deliver_btn_adb": {
            "label": "交付按钮ADB (绿色大按钮)",
            "type": "text",
            # 根据截图右下角估算
            "default": "input tap 1335 761"
        },
        
        # === 退场 ===
        "quit_adb": {
            "label": "退出界面ADB",
            "type": "text", 
            # 使用你之前提供的 reset_pos_exit_order 坐标
            "default": "input tap 1263 860"
        },
    }

    def execute(self):
        # 1. 解析参数
        slots = self.parse_list("slot_select_adbs")
        deliver_cmd = self.params.get("deliver_btn_adb")
        
        self.log(f"开始处理订单，共 {len(slots)} 个栏位")

        # 2. 循环处理每个栏位
        for i, slot_cmd in enumerate(slots):
            # 2.1 选中订单
            # self.log(f"检查订单 {i+1}...")
            execute_multiline_adb(slot_cmd)
            time.sleep(self.s_delay) # 等待右侧详情刷新
            
            # 2.2 尝试交付
            # 无论是否满足条件，点一下总是没错的。
            # 如果满足，就交了；如果不满足，点了也没反应。
            execute_multiline_adb(deliver_cmd)
            
            # 稍微停顿，防止点击过快系统反应不过来
            time.sleep(self.s_delay)


class DandelionTask(GameScriptBase):
    LABEL = "6. 蒲公英 (自动收发)"
    
    PARAM_CONFIG = {
        # === 进场 ===
        "area_adb": {
            "label": "进入蒲公英ADB (对应全局复位坐标)",
            "type": "text",
            "default": "input tap 1153 826\nsleep 2.5"
        },
        
        # === 核心动作 ===
        "harvest_btn_adb": {
            "label": "一键收获按钮ADB (图1右上青色按钮)",
            "type": "text",
            # 根据截图估算：右侧靠下上方一点
            "default": "input tap 1424 725"
        },
        "fill_btn_adb": {
            "label": "快速装填按钮ADB",
            "type": "text",
            # 根据截图估算：右侧最下方
            "default": "input tap 1407 825"
        },
        "submit_btn_adb": {
            "label": "弹窗提交按钮ADB",
            "type": "text",
            # 根据截图估算：弹窗的右下角
            "default": "input tap 974 703"
        },
        
        # === 退场 ===
        "quit_adb": {
            "label": "退出界面ADB (对应全局复位退出坐标)",
            "type": "text", 
            "default": "input tap 100 224"
        }
    }

    def execute(self):
        # 1. 进场 (Base类会自动调用 area_adb，但这里为了逻辑连贯清晰，我们显式打印一下)
        self.log(">>> 进入蒲公英小队...")
        
        # 2. 尝试收获
        # 无论有没有东西，点一下总是安全的
        self.log("动作: 点击一键收获")
        execute_multiline_adb(self.params.get("harvest_btn_adb"))
        time.sleep(self.s_delay) # 等待收获动画或提示消失
        
        # 3. 尝试装填
        self.log("动作: 点击快速装填")
        execute_multiline_adb(self.params.get("fill_btn_adb"))
        time.sleep(self.s_delay) # 等待弹窗出现
        
        # 4. 确认提交
        # 如果上一步没弹出窗（比如没东西可填），这一步点在空地上也没事
        self.log("动作: 点击确认提交")
        execute_multiline_adb(self.params.get("submit_btn_adb"))
        time.sleep(self.s_delay) # 等待提交动画

class WarehouseSaleTask(GameScriptBase):
    LABEL = "7. 仓库自动售卖"

    PARAM_CONFIG = {
        # === 1. 进场导航 (对应你的：选中仓库 -> 点击分类) ===
        # Base类会自动在复位后执行 area_adb
        "area_adb": {
            "label": "进场ADB (点击仓库 -> 点击分类)",
            "type": "text",
            "default": "input tap 1590 379\nsleep 2\ninput tap 1420 444\nsleep 1.5"
        },

        # === 2. 识别配置 (对应你的：识别框) ===
        "digit_crop_box": {
            "label": "数字识别框 [x1, y1, x2, y2]",
            "type": "string",
            "default": "[290, 382, 365, 412]"
        },
        
        # === 3. 判断条件 (对应你的：超过多少就卖) ===
        "sell_threshold": {
            "label": "售卖阈值 (库存 > 此数 则卖)",
            "type": "int",
            "default": "50"
        },

        # === 4. 售卖动作 (对应你的：卖的操作参数) ===
        "sell_action_adb": {
            "label": "售卖动作ADB (满足条件时执行)",
            "type": "text",
            "default": "input tap 339 328\nsleep 1\ninput tap 332 628\nsleep 1\ninput tap 957 622\nsleep 2"
        },

        # === 5. 退场 (对应你的：退场参数) ===
        # Base类会自动在 execute 执行完后调用 quit_adb
        "quit_adb": {
            "label": "退场ADB (点击关闭/返回)",
            "type": "text", 
            "default": "input tap 157 547\nsleep 1"
        }
    }

    def execute(self):
        # 此时 Base 类已经完成了 Reset 和 area_adb (进场)
        
        # --- 步骤 1: 截图识别 ---
        self.log(">>> 开始识别库存数字...")
        
        # 解析坐标
        crop_list = self.parse_list("digit_crop_box")
        crop_box = tuple(crop_list) if len(crop_list) == 4 else None
        
        if not crop_box:
            self.log("错误：未配置识别框坐标")
            return

        # 截图
        img_path = "sell_check.png"
        adb_screenshot(img_path, crop_box=crop_box)
        
        # AI 识别
        prompt = (
            "请识别图中的纯数字整数。"
            "如果包含斜杠(如 80/100)，只返回斜杠前面的数字。"
            "如果看起来像 'o' 或 'O'，请识别为 '0'。"
            "不要输出任何标点或文字，只返回数字。"
        )
        ai_res = query_vlm(img_path, prompt)
        
        # --- 步骤 2: 数据解析 ---
        try:
            # 简单清洗
            clean_res = ai_res.replace('o', '0').replace('O', '0')
            import re
            nums = re.findall(r'\d+', clean_res)
            
            # 没识别到给 -1，防止误卖
            current_count = int(nums[0]) if nums else -1
            self.log(f"AI返回: {ai_res} -> 识别库存: {current_count}")
            
        except Exception as e:
            self.log(f"解析数字失败: {e}")
            current_count = -1

        # --- 步骤 3: 逻辑判断 ---
        threshold = int(self.params.get("sell_threshold", 9999))
        
        # 逻辑：超过多少就卖 ( > )
        if current_count > threshold:
            self.log(f"条件满足: 库存 {current_count} > 阈值 {threshold}，执行售卖！")
            
            sell_cmd = self.params.get("sell_action_adb")
            execute_multiline_adb(sell_cmd)
            
            self.log("售卖动作执行完毕")
        else:
            self.log(f"条件不满足: 库存 {current_count} 未超过 {threshold}，跳过。")
            
        # 函数结束后，Base 类会自动执行 quit_adb
        

class CustomAdbTask(GameScriptBase):
    LABEL = "99. 自定义ADB脚本 (宏)"
    
    PARAM_CONFIG = {
        "adb_commands": {
            "label": "自定义指令 (支持 input tap/swipe, sleep, drag_path)",
            "type": "text", # 这会在UI显示为大文本框
            "default": (
                "# 示例：\n"
                "input tap 500 500\n"
                "sleep 1\n"
                "input swipe 800 500 200 500 1000\n"
                "# 拖拽动作 (仅限本项目特有指令)\n"
                "drag_path 100 100 200 200 300 300"
            )
        },
        "skip_reset": {
            "label": "是否跳过复位 (填 1 跳过，填 0 不跳过)",
            "type": "string", # 在UI里填 1 或 0
            "default": "0"
        },
        
    }
    # 重写复位逻辑：检测参数决定是否跳过
    def reset_state(self):
        is_skip = self.params.get("skip_reset", "0").strip()
        if is_skip == "1":
            self.log(">>> [设置] 已配置跳过复位步骤")
            return
        # 如果不是1，则调用父类的标准复位
        super().reset_state()
    def execute(self):
        commands = self.params.get("adb_commands", "")
        
        if not commands.strip():
            self.log("指令为空，跳过")
            return

        self.log(f"开始执行自定义ADB指令 ({len(commands.splitlines())} 行)...")
        
        # 直接调用你项目中已经写好的解析器
        # 它会自动处理 sleep, drag_path 和普通的 adb shell 指令
        execute_multiline_adb(commands)
        
        self.log("自定义指令执行完毕")
# === 注册表 ===
SCRIPT_REGISTRY = {
    t.LABEL: t for t in [
        FarmingTask, 
        GatheringTask, 
        ProcessingTask, 
        CookingTask, 
        OrderTask, 
        DandelionTask,
        WarehouseSaleTask,
        CustomAdbTask 
    ]
}

