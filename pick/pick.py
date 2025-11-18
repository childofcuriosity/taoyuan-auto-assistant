# pick/pick.py

def start_pick():
    print("【采集】开始")
    return True


def end_pick():
    print("【采集】结束")
    return True


# === 子功能模块 ===
# 你之后可以在这些文件里真正实现逻辑：
from pick.open_forest import open_forest
from pick.handle_forest import handle_forest
from pick.handle_bamboo import handle_bamboo
from pick.handle_xirang import handle_xirang
from pick.exit_interface import exit_interface
from pick.next_area import next_area


def pick():
    """
    pick 主流程 = 按流程图执行：
        start_pick
        → open_forest
        → handle_forest
        → next（第1次）→ handle_bamboo
        → next（第2次）→ handle_xirang
        → exit_interface
        → end_pick
    """
    if not start_pick():
        return True

    # 1. 打开伐木林
    if not open_forest():
        end_pick()
        return True

    # 2. 处理伐木林
    if not handle_forest():
        end_pick()
        return True

    # 3. 点击下一个（第1次）→ 竹林
    if not next_area():
        end_pick()
        return True
    if not handle_bamboo():
        end_pick()
        return True

    # 4. 点击下一个（第2次）→ 息壤
    if not next_area():
        end_pick()
        return True
    if not handle_xirang():
        end_pick()
        return True

    # 5. 退出界面
    if not exit_interface():
        end_pick()
        return True

    end_pick()
    return True
