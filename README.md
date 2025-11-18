

<p align="center">
  <img src="mascot.png" width="200" alt="桃源自动小助手">
</p>
<h1 align="center">🍃 桃源深处有人家 - 自动运营助手</h1>

<p align="center">
  基于 <strong>计算机视觉</strong> + <strong>大模型</strong> 的无人值守自动化运营系统
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue"/>
  <img src="https://img.shields.io/badge/Platform-Windows-green"/>
  <img src="https://img.shields.io/badge/Emulator-MuMu-orange"/>
  <img src="https://img.shields.io/badge/Model-VLM%20%2F%20ZhipuAI-purple"/>
</p>

---

## 📌 项目简介

本项目基于 **计算机视觉识别** 与 **自动化控制**，实现对《桃源深处有人家》的全自动运营。

核心策略如下：

* **资源不足 → 自动补种 / 投料**
* **资源过多 → 自动售卖**
* 系统循环执行「种地 → 采集 → 生产 → 清仓」四大流程，像生产线一样持续稳定运行。

---

## ✨ 功能亮点

### 🌱 自动种植

* 自动检测田地状态（是否可收获、是否需要播种）
* 自动收割 → 自动判断 → 自动播种
* 通过 VLM 准确识别土地状态，稳定可靠

### 🌳 自动采集

* 自动处理伐木林、竹林、息壤
* 根据识别结果判断是否需要采集
* 支持多轮连续采集流程

### 🏭 自动生产

覆盖全部生产建筑：

陶瓷 / 土料 / 玩具 / 编织 / 糕坊 / 木工 / 豆腐 / 腌制 / 饼坊 / 制糖 / 铡刀 / 豆坊 / 石磨 / 鸡舍等

* 自动收获产物
* 自动补料投产
* 按序遍历所有建筑，无需人工干预

### 🧹 自动清仓售卖

* 检测仓库容量
* 自动出售超过阈值的资源
* 始终保持仓库畅通

---

## 🎬 Demo 演示

📺 **[点此播放视频 Demo](https://www.bilibili.com/video/BV1KYyGBsExe)**
📄 **[点此查看程序输出日志 Demo](./demo.log)**

---

## 📮 反馈 & 交流群

QQ群：**1014644523**
群主即项目作者。

> TODO：作者是 23 级，目前游戏进度有限，因此生产设施支持范围基于现阶段认知。如果你在使用过程中愿意提供账号协助完善，欢迎联系我，让功能支持更全面、配置更自由。

---

# 🚀 快速开始

## 🖥️ 环境需求

1. Windows 系统电脑
2. 安装 **MuMu 模拟器**
3. 模拟器内安装《桃源深处有人家》
4. 模拟器窗口 **全屏模式（否则坐标会错位）**
5. 游戏内相机高度调至 **超远景**
6. 修改 `config.py`：

```python
os.environ["OPENAI_API_KEY"] = "你的智谱APIKey"
```

👉 [如何获取智谱 API Key](https://zhipu-ef7018ed.mintlify.app/cn/guide/start/quick-start)

---

## 🟩 方式一：运行源码

```bash
python main.py
```

缺哪个包就 `pip install` 哪个，依赖非常少。

---

## 🟦 方式二：直接使用可执行文件

* TODO：若有用户需要，我会提供打包好的 EXE 版本。

---

# 🔁 工作流程概览

> 小小感想：整个代码结构非常清晰，写出来时真的很享受这种“按想法落地”的过程。

```mermaid
graph TD
    start((开始)) --> farming[种地]
    farming --> pick[采集]
    pick --> production[生产]
    production --> sale[清仓]
    sale --> farming
```

---

# 🌱 种地流程

```mermaid
graph TD
    start_farm((开始)) --> check_status{查看状态} 
    check_status -->|等待| end_farm((结束))
    check_status -->|可收获| harvest[收获]
    harvest --> decide_plant{需要播种?}
    decide_plant -->|否| end_farm
    decide_plant -->|是| plant_action[播种] --> end_farm
```

### 状态识别流程

```mermaid
graph TD
    start_check((开始)) --> zoom_and_locate[缩放并定位蒲公英] 
    zoom_and_locate --> tap_field[点击田地] 
    tap_field --> screenshot[截屏] 
    screenshot --> build_prompt[构造 VLM Prompt] 
    build_prompt --> send_to_vlm[VLM 识别]  
    send_to_vlm --> extract_value[提取结果]  
    extract_value --> end_check((完成))
```

---

# 🌲 采集流程

```mermaid
graph TD
    start_pick((开始)) --> open_forest[伐木林]
    open_forest --> handle_forest[处理伐木林]
    handle_forest --> next_area[下一个] --第1次--> handle_bamboo[处理竹林]
    handle_bamboo --> next_area[下一个] --第2次--> handle_xirang[处理息壤]
    handle_xirang --> exit_interface[退出]
```

通用采集逻辑：

```mermaid
graph TD
    start_handle((开始)) --> check_status{查看状态} 
    check_status -->|等待| end_handle((结束))
    check_status -->|可收获| harvest[收获]
    harvest --> decide_pick{需要采集?}
    decide_pick -->|否| end_pick
    decide_pick -->|是| pick_action[采集] --> end_pick
```

---

# 🏭 生产流程

```mermaid
graph TD
    start_pro((开始)) --> open_hens[打开养鸡]
    open_hens --> step1[陶瓷] --> step2[土料] --> step3[玩具] --> step4[编织] --> step5[糕坊]
    step5 --> step6[木工] --> step7[豆腐加工] --> step8[腌制] --> step9[饼坊]
    step9 --> step10[制糖] --> step11[铡刀] --> step12[豆坊] --> step13[石磨]
    step13 --> step14[鸡舍] --> exit_pro[退出]
```

通用生产逻辑：

```mermaid
graph TD
    start_handle((开始)) --> try_harvest[尝试收获]
    try_harvest --> figure_state[检查状态]
    figure_state --> try_produce[尝试投产]
```

---

# 🧹 清仓流程

```mermaid
graph TD
    start_sale((开始)) --> open_host[打开仓库]
    open_host --> process_crop[处理作物]
    process_crop --> process_product[处理产品]
    process_product --> exit_sale[退出]
```

---

# 📌 License

本项目仅供学习、研究与技术探索使用。
请勿将脚本用于任何违反游戏规则或破坏游戏平衡的行为。
