# 文件: MyProject/src/ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.logic import AppLogic
from src.tasks import SCRIPT_REGISTRY

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("桃源助手专业版")
        self.geometry("950x650")
        
        self.logic = AppLogic()

        # === 布局结构 ===
        self.sidebar = tk.Frame(self, width=180, bg="#f0f0f0", relief="sunken", bd=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.content_area = tk.Frame(self, bg="white")
        self.content_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # 初始化
        self.create_sidebar()
        self.show_task_page() # 默认显示任务页

    def create_sidebar(self):
        btn_style = {"bg": "#e1e1e1", "relief": "flat", "height": 2}
        tk.Button(self.sidebar, text="配置填写", command=self.show_config_page, **btn_style).pack(fill=tk.X, padx=5, pady=5)
        tk.Button(self.sidebar, text="任务列表", command=self.show_task_page, **btn_style).pack(fill=tk.X, padx=5, pady=5)

    def clear_content(self):
        for w in self.content_area.winfo_children():
            w.destroy()
# ================= 页面 1：配置填写 (修改版) =================
    def show_config_page(self):
        self.clear_content()
        
        # 1. 标题
        tk.Label(self.content_area, text="全局配置", font=("微软雅黑", 16, "bold"), bg="white").pack(pady=15)
        
        # 2. 创建滚动容器
        canvas = tk.Canvas(self.content_area, bg="white", highlightthickness=0)
        scroll = ttk.Scrollbar(self.content_area, command=canvas.yview)
        
        frame = tk.Frame(canvas, bg="white")
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scroll.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 第一组：基础环境 ---
        g_env = tk.LabelFrame(frame, text="基础连接与AI", bg="white", font=("微软雅黑", 10, "bold"), padx=10, pady=10)
        g_env.pack(fill=tk.X, pady=10)
        
        # [已删除] 窗口名称
        
        # API Key (行号移到了 0)
        self._input(g_env, "API Key", "OPENAI_API_KEY", 0)
        
        # ADB 选择器 (行号移到了 1)
        tk.Label(g_env, text="ADB路径:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
        entry_adb = tk.Entry(g_env, width=40, bg="#f9f9f9")
        entry_adb.insert(0, self.logic.config.get("adb_path", ""))
        entry_adb.grid(row=1, column=1, sticky="w", pady=5)
        entry_adb.bind("<FocusOut>", lambda e: self.logic.update_config("adb_path", entry_adb.get()))
        tk.Button(g_env, text="浏览", command=lambda: self._sel_file(entry_adb)).grid(row=1, column=2, padx=5)

        # --- [已删除] 第二组：自动化阈值 ---

        # --- 第三组：延迟 ---
        g_del = tk.LabelFrame(frame, text="延迟设置 (秒)", bg="white", font=("微软雅黑", 10, "bold"), padx=10, pady=10)
        g_del.pack(fill=tk.X, pady=10)
        self._input(g_del, "小延迟", "small_delay", 0, 0)
        self._input(g_del, "大延迟", "big_delay", 0, 2)

        # === 复位坐标设置 ===
        g_reset = tk.LabelFrame(frame, text="复位逻辑坐标 (x y)", bg="white", font=("微软雅黑", 10, "bold"), padx=10, pady=10)
        g_reset.pack(fill=tk.X, pady=10)
        
        self._input(g_reset, "订单图标", "reset_pos_order", 0, 0)
        self._input(g_reset, "退出订单", "reset_pos_exit_order", 0, 2)
        self._input(g_reset, "蒲公英图标", "reset_pos_dandelion", 1, 0)
        self._input(g_reset, "退出蒲公英", "reset_pos_exit_dandelion", 1, 2)

        # --- 底部保存按钮区域 ---
        btn_area = tk.Frame(frame, bg="white", pady=20)
        btn_area.pack(fill=tk.X)

        tk.Button(btn_area, text="💾 保存并应用配置", bg="#007bff", fg="white", 
                  font=("微软雅黑", 12, "bold"), width=25, height=2,
                  command=self.save_config_manual).pack()
        
        tk.Label(btn_area, text="* 提示：配置会自动保存，点击按钮可强制刷新环境变量", fg="gray", bg="white").pack(pady=5)

    # --- 新增：按钮点击事件 ---
    def save_config_manual(self):
        """手动保存按钮的逻辑"""
        # 1. 强制让当前焦点控件失去焦点 (这样能触发输入框的 <FocusOut> 事件，确保数据被写入 logic)
        self.focus_set()
        
        # 2. 再次调用 logic 的保存和应用环境方法
        self.logic.save_data()
        self.logic.apply_config_to_env()
        
        # 3. 弹窗提示
        messagebox.showinfo("成功", "✅ 全局配置已保存并生效！")

    def _input(self, parent, label, key, r, c=0):
        tk.Label(parent, text=f"{label}:", bg="white").grid(row=r, column=c, sticky="e", padx=5, pady=5)
        e = tk.Entry(parent, width=20, bg="#f9f9f9")
        e.insert(0, self.logic.config.get(key, ""))
        e.grid(row=r, column=c+1, sticky="w", padx=5)
        e.bind("<FocusOut>", lambda ev: self.logic.update_config(key, e.get()))

    def _sel_file(self, entry):
        path = filedialog.askopenfilename(filetypes=[("EXE", "*.exe")])
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
            self.logic.update_config("adb_path", path)

    # ================= 任务页面 =================
    def show_task_page(self):
        self.clear_content()
        
        # 顶部栏
        top = tk.Frame(self.content_area, bg="white")
        top.pack(fill=tk.X, padx=20, pady=10)
        tk.Button(top, text="+ 新建任务", bg="#28a745", fg="white", command=self.add_task).pack(side=tk.LEFT)
        tk.Button(top, text="▶ 全部启动", bg="#007bff", fg="white", command=self.run_all).pack(side=tk.LEFT, padx=10)

        # 滚动列表
        canvas = tk.Canvas(self.content_area, bg="white", highlightthickness=0)
        scroll = ttk.Scrollbar(self.content_area, command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="white")
        
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.scroll_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scroll.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.refresh_list()

    def refresh_list(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        for i, t in enumerate(self.logic.tasks):
            self.create_card(i, t)
# === 核心：卡片绘制 (样式修复版) ===
    def create_card(self, idx, data):
        # 1. 卡片整体容器 (加深边框，增加阴影感)
        card = tk.Frame(self.scroll_frame, bg="white", bd=2, relief="groove")
        card.pack(fill=tk.X, pady=10, ipady=5, padx=5) # 增加 padx 避免贴边

        # === Row 1: 标题栏 (浅灰色背景) ===
        r1 = tk.Frame(card, bg="#f0f0f0", height=35)
        r1.pack(fill=tk.X)
        
        # ID 和 标题
        tk.Label(r1, text=f" 任务 #{data['id']} ", font=("微软雅黑", 10, "bold"), bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=5, pady=5)
        
        # 右侧按钮组
        bg = tk.Frame(r1, bg="#f0f0f0")
        bg.pack(side=tk.RIGHT, padx=5)
        
        # 删除按钮
        tk.Button(bg, text="✕", font=("Arial", 10, "bold"), fg="#dc3545", bd=0, bg="#f0f0f0", cursor="hand2",
                  command=lambda: self.del_task(idx)).pack(side=tk.RIGHT, padx=5)
        
        # 启用开关
        enable_var = tk.BooleanVar(value=data["enable"])
        tk.Checkbutton(bg, text="启用", variable=enable_var, bg="#f0f0f0", font=("微软雅黑", 9),
                       command=lambda: self.logic.update_task_status(idx, enable_var.get())).pack(side=tk.RIGHT, padx=5)
        
        # 启动按钮
        tk.Button(bg, text="▶ 运行此任务", bg="#17a2b8", fg="white", relief="flat", font=("微软雅黑", 9), padx=5,
                  command=lambda: self.run_single(idx)).pack(side=tk.RIGHT, padx=10)

        # === Row 2: 任务类型选择 (单独一行，醒目) ===
        r2 = tk.Frame(card, bg="white", pady=5, padx=10)
        r2.pack(fill=tk.X)
        
        tk.Label(r2, text="任务类型:", bg="white", font=("微软雅黑", 9, "bold")).pack(side=tk.LEFT)
        
        cb = ttk.Combobox(r2, values=self.logic.get_available_types(), state="readonly", width=30)
        cb.set(data["type"])
        cb.pack(side=tk.LEFT, padx=10)

        # === Row 3: 参数配置区 (重点修改区域) ===
        # 使用 LabelFrame 将参数包裹起来，显得整洁
        f_param_container = tk.LabelFrame(card, text="详细参数配置", bg="white", fg="#666", font=("微软雅黑", 9), padx=10, pady=10)
        f_param_container.pack(fill=tk.X, padx=10, pady=10)

        # 内部渲染函数
        def render_params():
            # 清空旧控件
            for w in f_param_container.winfo_children(): w.destroy()
            
            task_type = data["type"]
            params_data = data["params"]
            
            cls = SCRIPT_REGISTRY.get(task_type)
            if not cls: return
            
            config_def = cls.PARAM_CONFIG
            
            if not config_def:
                tk.Label(f_param_container, text="( 此任务类型无需额外配置 )", bg="white", fg="#999").pack(anchor="w")
                return

            # 遍历配置，垂直排列 (Label在上，Input在下)
            for key, conf in config_def.items():
                val = params_data.get(key, conf.get("default", ""))
                label_text = conf.get("label", key)
                input_type = conf.get("type", "string")

                # 1. 每一个参数包裹在一个 Frame 里，方便布局
                p_row = tk.Frame(f_param_container, bg="white")
                p_row.pack(fill=tk.X, pady=5) # 垂直堆叠，增加间距

                # 2. 标签 (左对齐，加粗)
                tk.Label(p_row, text=label_text, bg="white", font=("微软雅黑", 9, "bold"), fg="#333").pack(anchor="w")

                # 3. 输入控件 (根据类型判断)
                if input_type == "text":
                    # === 多行文本框 (ADB语法专用) ===
                    # 黑色边框，高度设为4行
                    text_widget = tk.Text(p_row, height=4, font=("Consolas", 9), relief="solid", bd=1)
                    text_widget.insert("1.0", str(val))
                    text_widget.pack(fill=tk.X, pady=(2, 0)) # 填满横向宽度
                    
                    # 绑定保存逻辑
                    def save_text(e, k=key, w=text_widget):
                        # 获取内容时去除末尾自动添加的换行符
                        content = w.get("1.0", "end-1c")
                        self.logic.update_task_param(idx, k, content)
                    text_widget.bind("<FocusOut>", save_text)
                    
                    # 提示文字
                    tk.Label(p_row, text="* 支持多行输入，按回车换行", bg="white", fg="#999", font=("Arial", 8)).pack(anchor="w")

                else:
                    # === 普通单行输入框 (int 或 string) ===
                    entry = tk.Entry(p_row, bg="#f9f9f9", font=("Consolas", 9), relief="sunken")
                    entry.insert(0, str(val))
                    entry.pack(fill=tk.X, pady=(2, 0)) # 填满横向宽度
                    
                    def save_entry(e, k=key, w=entry):
                        self.logic.update_task_param(idx, k, w.get())
                    entry.bind("<FocusOut>", save_entry)

        # 初次渲染
        render_params()

        # 类型切换事件
        def on_change(event):
            if cb.get() != data["type"]:
                self.logic.update_task_type(idx, cb.get())
                self.refresh_list() # 必须刷新整个列表以重新计算高度
        cb.bind("<<ComboboxSelected>>", on_change)

    # === 动作 ===
    def add_task(self):
        self.logic.add_task()
        self.refresh_list()

    def del_task(self, idx):
        if messagebox.askyesno("确认", "删除此任务？"):
            self.logic.remove_task(idx)
            self.refresh_list()

    def run_single(self, idx):
        res = self.logic.run_single_task(idx)
        print(res) # 控制台打印
        messagebox.showinfo("运行结果", res)

    def run_all(self):
        res = self.logic.run_all_tasks()
        messagebox.showinfo("运行结果", res)