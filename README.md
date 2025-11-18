
<p align="center">
  <img src="mascot.png" width="200" alt="桃源自动小助手">
</p>
<h1 align="center">🍃 桃源深处有人家 - 自动运营助手</h1>

<p align="center">
  基于计算机视觉 + 大模型的全自动运营系统
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue"/>
  <img src="https://img.shields.io/badge/Platform-Windows-green"/>
  <img src="https://img.shields.io/badge/Emulator-MuMu-orange"/>
  <img src="https://img.shields.io/badge/Model-VLM%20%2F%20ZhipuAI-purple"/>
</p>

---

## 📌 项目简介

本项目利用 **计算机视觉识别** 与 **自动化控制**，实现无人值守的自动化游戏运营。

核心策略：

* **资源不足 → 自动补种/补料**
* **资源过多 → 自动售卖**

系统会循环执行 *种地 → 采集 → 生产 → 清仓* 四大流程，像工厂一样稳定运行。

---

## ✨ 功能亮点

### 🌱 自动种植

* 自动判断田地是否可收获
* 自动收割 → 自动判断 → 自动播种
* 通过 VLM 识别土地状态，准确率高

### 🌳 自动采集

* 自动处理：伐木林、竹林、息壤
* 识别资源状态 → 选择是否采集

### 🏭 自动生产

支持全部生产建筑：
陶瓷 / 土料 / 玩具 / 编织 / 糕坊 / 木工 / 豆腐 / 腌制 / 饼坊 / 制糖 / 铡刀 / 豆坊 / 石磨 / 鸡舍等

* 自动收获
* 自动投料生产

### 🧹 自动清仓售卖

* 检测库存上限
* 自动卖掉“超过阈值”的物品
* 保持仓库流通

---

## 🎬 Demo 演示

📺 **[点击播放视频 demo](./demo.mp4)**
 **[点击查看视频对应程序输出 demo](./demo.log)**

---

## 📮 反馈 & 交流群

QQ群：**1014644523**
群主是作者。

- TODO:作者是23级，所以目前生产范围限制在这个水平，多的不清楚机制了，如果这个项目有人用，请联系我让我有动力和用您贡献的账号去完善，让每个人都能自定义配置

---

# 🚀 快速开始

## 🖥️ 环境要求

1. 一台 Windows 电脑
2. 安装 **MuMu 模拟器**
3. 模拟器中安装 **《桃源深处有人家》**
4. 将 MuMu 模拟器窗口**全屏（不要留白边）**
5. 在游戏内设置相机高度为**超远景** 
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

缺啥包就 `pip install` 哪个，依赖极少。



## 🟦 方式二：下载可执行文件

- TODO：如果有人会用，我后续有空打包一个。

---

# 🔁 工作流程概览

碎碎念：我的代码结构很清晰，按想法写出来的过程简直是一种享受


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
    screenshot --> build_prompt[构造VLM prompt] 
    build_prompt --> send_to_vlm[VLM识别]  
    send_to_vlm --> extract_value[提取状态]  
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
    figure_state --> try_produce[尝试生产]
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

本项目仅供学习与技术研究使用，请勿将脚本用于任何违反游戏规则或破坏游戏平衡的行为。

