from sale.sale_utils import *

def start_sale():
    print("【清仓大甩卖】开始")
    return True

def end_sale():
    print("【清仓大甩卖】结束")
    return True

def open_host():
    print("打开谷仓")
    zoom_and_locate()
    time.sleep(eval(os.environ.get("small_delay")))
    drag_ratio(0.7, 0.5, 0.3, 0.5)
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.6366,0.4619)
    time.sleep(eval(os.environ.get("small_delay")))
    return True


def process_crop(num_param=None):
    num = num_param or int(os.environ.get("plant_num_sale"))
    print("处理作物")
    
    while process(0.8902,0.4921,"作物",num_limit=num):
        pass
    return True
    



def process_product(num_param=None):
    num = num_param or int(os.environ.get("produce_num_sale"))
    print("处理产品")
    while process(0.8902,0.6405,"产品",num_limit=num):
        pass
    return True

def exit_interface():
    print("退出界面")
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.0518, 0.3294)  # 点击关闭按钮
    time.sleep(eval(os.environ.get("small_delay")))
    return True

# ===== 主流程（严格按流程图顺序） =====

def sale():
    if not start_sale():
        return True
    # 1. 打开谷仓
    if not open_host():
        end_sale()
        return True
    # 2. 处理作物
    if not process_crop():
        end_sale()
        return True
    # 3. 处理产品
    if not process_product():
        end_sale()
        return True
    # 4. 退出界面
    if not exit_interface():
        end_sale()
        return True
    return True
    
if __name__ == "__main__":
    open_host()