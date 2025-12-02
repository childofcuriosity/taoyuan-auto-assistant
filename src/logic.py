# 文件: MyProject/src/logic.py
import json
import os
from src.tasks import SCRIPT_REGISTRY
class AppLogic:
    def __init__(self):
        self.data_file = "data.json"
        
        # === 1. 定义默认全局配置 ===
        self.config = {
            # --- 基础连接 ---
            "window_name": "MuMu安卓设备",
            "adb_path": r"C:\Program Files\Netease\MuMu\nx_main\adb.exe",
            "OPENAI_API_KEY": "",
            
            # --- 数量限制 ---
            "plant_num_limit": "20",
            "produce_num_limit": "8",
            "plant_num_sale": "40",
            "produce_num_sale": "10",
            
            # --- 延迟设置 ---
            "small_delay": "1.5",
            "big_delay": "8",

            # === 新增：复位逻辑坐标 (空格分隔 x y) ===
            "reset_pos_order": "1273 829",       # 订单图标
            "reset_pos_exit_order": "1263 860",  # 退出订单
            "reset_pos_dandelion": "1153 826",   # 蒲公英图标
            "reset_pos_exit_dandelion": "100 224" # 退出蒲公英
        }
        
        self.tasks = []
        self.load_data()
        self.apply_config_to_env()

    def get_available_types(self):
        return list(SCRIPT_REGISTRY.keys())

    def get_default_params(self, task_type):
        """从 PARAM_CONFIG 中提取 {key: default_value}"""
        cls = SCRIPT_REGISTRY.get(task_type)
        if not cls: return {}
        
        defaults = {}
        # 遍历配置字典，提取 default 字段
        for key, conf in cls.PARAM_CONFIG.items():
            defaults[key] = conf.get("default", "")
        return defaults

    def add_task(self):
        new_id = len(self.tasks) + 1
        default_type = self.get_available_types()[0]
        new_task = {
            "id": new_id,
            "name": f"任务 {new_id}",
            "type": default_type,
            "params": self.get_default_params(default_type),
            "enable": False
        }
        self.tasks.append(new_task)
        self.save_data()
        return new_task

    def update_task_type(self, index, new_type):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["type"] = new_type
            self.tasks[index]["params"] = self.get_default_params(new_type)
            self.save_data()

    def update_task_param(self, index, key, value):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["params"][key] = value
            self.save_data()

    def update_task_status(self, index, is_enable):
        self.tasks[index]["enable"] = is_enable
        self.save_data()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_data()

    def update_config(self, key, value):
        self.config[key] = value
        self.save_data()
        self.apply_config_to_env()

    def apply_config_to_env(self):
        """将配置注入到系统环境变量"""
        for k, v in self.config.items():
            os.environ[k] = str(v)

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({"config": self.config, "tasks": self.tasks}, f, ensure_ascii=False, indent=4)

    # 唯一需要注意的是 load_data，建议保持之前的“清洗逻辑”
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config = data.get("config", self.config)
                    
                    tasks = data.get("tasks", [])
                    cleaned = []
                    for t in tasks:
                        # 确保 params 是字典
                        if not isinstance(t.get("params"), dict):
                            t_type = t.get("type", self.get_available_types()[0])
                            t["type"] = t_type
                            t["params"] = self.get_default_params(t_type)
                        cleaned.append(t)
                    self.tasks = cleaned
            except Exception as e:
                print(f"数据重置: {e}")
                self.tasks = []

    # 运行逻辑保持不变
    def run_single_task(self, index):
        self.apply_config_to_env()
        task = self.tasks[index]
        cls = SCRIPT_REGISTRY.get(task["type"])
        if not cls: return "未知任务类型"
        
        try:
            instance = cls(task["params"])
            instance.run()
            return f"[{task['name']}] 执行完毕"
        except Exception as e:
            return f"执行出错: {e}"
            
    def run_all_tasks(self):
        self.apply_config_to_env()
        count = 0
        for i, t in enumerate(self.tasks):
            if t["enable"]:
                self.run_single_task(i)
                count += 1
        return f"已执行 {count} 个任务"
