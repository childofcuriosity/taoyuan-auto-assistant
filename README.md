[中文版](README_zh.md)

<p align="center">
  <img src="mascot.png" width="200" alt="Taoyuan Auto Assistant">
</p>
<h1 align="center">🍃 Taoyuan Shenchu You Renjia - Automated Operations Assistant</h1>

<p align="center">
  An unattended automation system powered by <strong>emulator control</strong> + <strong>vision-language models</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue"/>
  <img src="https://img.shields.io/badge/Emulator-MuMu-orange"/>
  <img src="https://img.shields.io/badge/AI-Zhipu%20GLM--4V-purple"/>
</p>

Keywords: Taoyuan Shenchu You Renjia assistant, automatic harvesting, idle scripts, Python automation, Android emulator scripts.

---
## 📢 V2.7 Update Highlights
v2.7 adds scheduled startup.

## 📢 V2.6 Update Highlights
In v2.6, @Mufanc stepped in and thoroughly optimized the underlying phone-control implementation, fully resolving instability issues such as multi-touch.

## 📢 V2.5 Update Highlights
v2.5 adds user-defined command tasks and an option to skip the reset logic, making it easier for the community to build scripts for various events. Scripts can be run as specified by their creators.

v2.5.1 improves crop-state recognition, adds support for custom screenshot regions and prompts, and improves the default prompt. Missing new parameters are now automatically merged in the underlying configuration.

## 📢 V2.4 Update Highlights
v2.4 adds selling items from storage.

## 📢 V2.3 Update Highlights
v2.3 improves the farming recognition prompt for greater accuracy.

## 📢 V2.2 Update Highlights
v2.2 adjusts the logic to handle randomized cooking positions.

v2.2.1 likely fixes the message401 error.
v2.2.2 adds a button in the UI to save task configurations.
v2.2.3 cleans up code formatting (no effect on program behavior).

## 📢 V2.1 Update Highlights
v2.1 improves recognition through optimized prompts and cropping parameters.

## 📢 V2 Update Highlights

The project has undergone a major refactor, with the following core improvements:

1.  **Completely mouse-free**: Uses background ADB commands for control. **The script does not occupy your mouse while running**, so you can use other windows on your computer while it runs unattended.
2.  **Graphical interface**: Adds a Tkinter UI, so you no longer need to edit parameters in the code.
3.  **Custom positions**: All tap coordinates and swipe paths can be freely configured in the UI to suit different devices.

---
## 🎬 Demo and Tutorials

📺 **[Watch the Demo](https://www.bilibili.com/video/BV1jkStBwEyh)**
📺 **[Watch the Tutorial](https://www.bilibili.com/video/BV1XrSYBTETe/)**
📺 **[Watch the Tutorial on New v2.5 Features](https://www.bilibili.com/video/BV1f3BXBuEYX/)**
📘 **[Written Source Code Walkthrough (Zhihu)](https://zhuanlan.zhihu.com/p/1980082268472107335)**
📺 **[Video Source Code Walkthrough (Bilibili)](https://www.bilibili.com/video/BV1Dt2BB6Esu)**


## ✨ Core Features

### 1. 🌾 Smart Farming
* **Smart replanting**: Uses a VLM to identify inventory in the crop bar, automatically calculate shortages, and prioritize crops with the lowest stock.
* **Continuous operation**: Automatically identifies field states (ripe/empty) to cycle between harvesting and planting.

### 2. 🌲 Multi-site Gathering
* **Automatic patrol**: Supports multiple configurable gathering sites (logging forest, bamboo grove, Xirang, etc.) and automatically switches scenes.
* **Dynamic decisions**: Analyzes screenshots of each gathering site, distinguishes between “Harvest,” “Produce,” and “Working” states, and automatically performs the corresponding actions.

### 3. 🏭 Production Line Processing
* **Standard/special workshop support**: Automatically adapts to the operating logic of standard workshops (such as mills) and special workshops (such as chicken coops).
* **Smart production**: Automatically harvests $\rightarrow$ checks raw material inventories $\rightarrow$ produces the item with the greatest shortage.

### 4. 🍳 Batch Cooking
* **Individual resets**: Supports reset logic for each dish to prevent misalignment caused by scrolling the list.
* **Batch preparation**: Automatically taps repeatedly to cook when low stock is detected.

### 5. 📜 Automatic Orders
* **One-click delivery**: Automatically checks order slots and delivers as soon as the requirements are met.

### 6. 🌬️ Dandelion Dispatch and Collection
* **Complete workflow**: Automatically enters the Dandelion Squad $\rightarrow$ collects everything with one tap $\rightarrow$ quickly loads supplies $\rightarrow$ confirms departure.

### 7. 💰 Smart Selling
* **Directly sell wheat and other items**: Supports custom inventory thresholds, automatically recognizes current quantities using OCR, and precisely calculates and sells the surplus.

### 8. 🧩 Custom Extensions
* **Community contributions**: Provides a standardized command interface and supports importing user-written scripts for specific events (such as limited-time tasks), enabling quick sharing and reuse of logic.
* **Flexible execution**: Removes the requirement for mandatory initialization by supporting a configurable “Skip Reset” mode. Scripts can start directly from the current UI state, with the execution environment specified by their creators, enabling plug-and-play use in complex scenarios.

---

## 📝 Configuration Guide

### 1. Configuration Files Explained
*   **`data.json`**: The **user configuration** that the program actually reads. All settings edited and saved in the UI are stored here.
*   **`最终参数.json`**: A **full-featured reference configuration** provided by the author (based on a 1600x900 resolution). First-time users are encouraged to consult this file to learn the parameter structure or use it to restore a configuration that has become disorganized.

### 2. How Saving Works
*   **Automatic saving**: After editing a setting, you must **click another blank area in the UI** (so the current input field loses focus) for the program to trigger automatic saving.
*   **Manual saving**: After editing all settings, you can also click the “**Save and Apply Configuration**” button at the bottom of the UI to force a save and refresh the settings.

### 3. List Formatting
When entering list parameters in the configuration UI, always separate items with **English commas** `,`.
*   ✅ Correct: `['清汤白菜', '蛋炒饭']`
*   ❌ Incorrect: `['清汤白菜'， '蛋炒饭']` (uses a Chinese comma)

### 4. Configuration and Initialization Recommendations
*   **First-time use**: Rename `最终参数.json` in the project directory to `data.json` so that the software opens with the full-featured default configuration.
*   **Backups**: After configuring parameters for your setup, make a backup copy of `data.json`. If the configuration becomes disorganized later, simply rename the backup to `data.json` and place it in the project root to restore it.

### 5. ⚠️ Important Operating Warning
On the “Task List” screen, scrolling the **mouse wheel** over the “Task Type” dropdown directly changes the task type.
*   **Consequence**: Changing the type **immediately resets and clears** all parameter settings for that task!
*   **Recommendation**: Use the scroll wheel carefully when browsing the list to avoid accidentally changing a dropdown and losing your configuration.



---

## 📖 Custom Command Tutorial (ADB Syntax)

In the software's “Configuration Entry” screen, you can enter custom commands to control script behavior. The following syntax is supported:

*   **Tap**: `input tap <x> <y>`
    *   Example: `input tap 500 500` (tap the center of the screen)
*   **Swipe**: `input swipe <x1> <y1> <x2> <y2> <duration_ms>`
    *   Example: `input swipe 800 500 200 500 1000` (swipe from right to left over 1 second)
    ⚠️ Operating warning: Use longer, slower swipes. Otherwise, inconsistent momentum can cause large coordinate errors.
*   **Wait**: `sleep <seconds>`
    *   Example: `sleep 1.5` (wait 1.5 seconds for a popup or animation)
*   **Path drag** (specific to this project): `drag_path <x1> <y1> <x2> <y2> ...`
    *   Used for planting and harvesting; simulates holding a finger down and dragging through each coordinate in sequence.
    *   Example: `drag_path 100 100 200 200 300 300`

---

---

## ⚠️ Recommended Setup Before Running


MuMu Emulator is supported.
To reduce the amount of configuration editing, the following emulator and game settings are recommended:

1.  **Resolution**: Set the emulator resolution to **1600 x 900 (DPI 240)**.
    *   *Note: The default parameters were recorded at this resolution. If you use a different resolution, you must manually update all coordinate parameters in the software's configuration UI.*
    *   *Note: Set the frame rate above 30 FPS and disable frame-rate reduction in the background.*
2.  **Zoom**: Although the script includes automatic zooming out, game loading delays can affect it. **Manually pinch with two fingers to zoom all the way out before running** to ensure correct behavior.
3.  **Coordinate tool**: To make configuration editing easier, enable **Pointer Location** in the emulator:
    *   *How*: Open Android Settings -> About Phone -> Tap “Build Number” 7 times -> Go back to “System - Developer Options” -> Find and enable **“Pointer Location”**.
    *   *Result*: When enabled, clicking the emulator screen displays the exact (X, Y) coordinates at the top, making it easier to enter them in the configuration.
4.  **Game settings**:
    *   Camera height: **Very Far View**.
    *   Screen scrolling: **Fast**.
## 🚀 Quick Start

### 1. ⚠️ Setup Before Running (Required Reading)
Refer to the preceding section, **“Recommended Setup Before Running.”**

### 2. Obtain an API Key
This project uses **Zhipu AI (GLM-4V)** for image recognition. Apply for an API key on the Zhipu Open Platform.
👉 [How to Obtain a Zhipu API Key](https://zhipu-ef7018ed.mintlify.app/cn/guide/start/quick-start)

### 3. Locate ADB
Find the path to the `adb.exe` file included with your emulator:
*   Right-click the **MuMu Emulator** desktop icon -> Select **“Open file location.”**
*   Find `adb.exe` in that folder (if Windows hides the .exe extension, open “View” in File Explorer and enable “File name extensions” to show all extensions).

### 4. Run the Program
Choose a startup method that suits your needs:

#### 🟩 Method 1: Run from Source (Recommended for Developers)
1.  Make sure Python 3.10+ is installed on your computer.
2.  Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the script:
    ```bash
    python main.py
    ```

#### 🟦 Method 2: Run the EXE (Recommended for Beginners)
*   Download the latest packaged program archive from the shared files in **QQ Group (1014644523)**.
*   Double-click the `.exe` to run it directly; no Python installation is required.

---

## 🛠️ Project Structure
### 📂 Source Version
```text
TAOYUAN/
├── main.py              # Entry point
├── build.spec           # PyInstaller build configuration (key source file). Developers can package the EXE with pyinstaller build.spec
├── requirements.txt     # Dependencies (for environment setup)
├── README.md            # Project documentation
├── app.ico              # Application icon (used by the .exe)
├── mascot.png           # Project display logo
├── 最终参数.json         # Default full-featured reference configuration (recommended for beginners)
├── data.json            # Your configuration (generated at runtime/manually renamed; not uploaded)
└── src/                 # Core source package
    ├── ui.py            # Graphical interface (dynamically built with Tkinter)
    ├── logic.py         # Business logic and data persistence
    ├── tasks.py         # Implementation of the six main tasks
    ├── adb_utils.py     # ADB communication, screenshots, and multi-touch wrappers
    └── ai_client.py     # VLM interface
```
### 📦 EXE Release Version (As Received by Users)
```text
TAOYUAN/
├── TaoyuanHelper.exe    # Double-click to run
├── data.json            # Your configuration (generated at runtime/manually renamed; not uploaded)
├── 最终参数.json         # Default full-featured reference configuration (recommended for beginners)
└── README.md            # User guide
```
---

## 📮 Community Group

QQ Group: **1014644523**


## 📮 Q&A

### Q1: A growing crop is selected, the AI returns “plant” when queried, and the script starts planting. Why?

A: A workshop on the screen may contain something that looks like a plant ready to harvest (such as pickled cabbage). Try moving these workshops outside the screenshot region.

---

# 📌 License

This project is intended for learning, research, and technical exploration only.
Please do not use the script for any behavior that violates the game's rules or disrupts game balance.
