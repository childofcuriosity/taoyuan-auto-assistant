# from config import *
# production/production.py
from production.production_utils import *
def start_production():
    print("【生产】开始")
    return True

def end_production():
    print("【生产】结束")
    return True


# ===== 子功能 =====

def open_hens():
    print("打开养鸡界面")
    zoom_and_locate()
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.6942,0.8206)
    time.sleep(eval(os.environ.get("big_delay")))
    return True

def last_area():
    print("点击『上一个』")
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.0634,0.7333)
    time.sleep(eval(os.environ.get("small_delay")))
    return True

def handle_ceramics():
    print("处理陶瓷")
    goods_list=["陶器","单色瓷"]
    handle_area(goods_list)
    return True

def handle_clay():
    print("处理土料")
    goods_list=["陶土","釉料"]
    handle_area(goods_list)
    return True

def handle_toys():
    print("处理玩具")
    goods_list=["竹蜻蜓","泥哨","竹板"]
    handle_area(goods_list)
    return True

def handle_weaving():
    print("处理编织")
    goods_list=["竹片","竹篓","麻绳"]
    handle_area(goods_list)
    return True

def handle_pastry():
    print("处理糕坊")
    goods_list=["糯米糕","鸡蛋糕","发糕"]
    handle_area(goods_list)
    return True

def handle_carpentry():
    print("处理木工")
    goods_list=['陶艺木具','榫卯','鲁班锁']
    handle_area(goods_list)
    return True

def handle_tofu():
    print("处理豆腐加工")
    goods_list=['油豆腐','腐竹','豆腐乳','豆筋','豆腐脑','豆腐干']
    handle_area(goods_list)
    return True

def handle_pickling():
    print("处理腌制")
    goods_list=['咸鸡蛋','酸菜','腌鸡肉','腌土豆']
    handle_area(goods_list)
    return True

def handle_pie():
    print("处理饼坊")
    goods_list=['鸡蛋饼','烧饼','蔬菜饼','土豆饼']
    handle_area(goods_list)
    return True

def handle_sugar():
    print("处理制糖")
    goods_list=['糖','红糖','麦糖']
    handle_area(goods_list)
    return True

def handle_chopper():
    print("处理铡刀")
    goods_list=['鸡饲料']
    handle_area(goods_list)
    return True

def handle_beans():
    print("处理豆坊")
    goods_list=['豆腐','豆浆','豆豉']
    handle_area(goods_list)
    return True

def handle_stone_mill():
    print("处理石磨")
    goods_list=['面粉','糕粉','土豆粉']
    handle_area(goods_list)
    return True

def handle_chicken_coop(num_param=None):
    num = num_param or int(os.environ.get("produce_num_limit"))
    print("处理鸡舍")
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.8290,0.8198)
    time.sleep(eval(os.environ.get("small_delay")))
    image_path = screenshot()  
    instruction = f"界面右下角有2个产品，对应的名称依次是['鸡蛋','鸡肉']。"
    instruction1="每个产品右边数字表示库存个数，请你识别每个产品的库存个数并且作为列表返回，格式为[鸡蛋个数，鸡肉个数]。不要有其他多余说明。"
    prompt1 = build_prompt(image_path, instruction + instruction1)
    vlm_response1 = send_to_vlm(prompt1)
    goods_nums=parse_vlm_inventory(vlm_response1)
    if isinstance(goods_nums, str):
        print(f"【生产】VLM 返回无法解析的结果：{goods_nums}")
        return True
    if goods_nums[0]>=num and goods_nums[1]>=num:
        print("鸡蛋和鸡肉库存均已充足，无需生产")
        return True
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.6834, 0.8222)  # 点击喂食按钮
    time.sleep(eval(os.environ.get("small_delay")))
    return True

def exit_interface():
    print("退出界面")
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.1092,0.1937)  
    time.sleep(eval(os.environ.get("small_delay")))
    return True


# ===== 主流程（严格按流程图顺序） =====

def production():
    """
    生产流程 = 按流程图执行：
        start → 打开养鸡 → 上一个 → handle_xx（共14次） → 退出界面 → end
    """

    if not start_production():
        return True

    # 1. 打开养鸡
    if not open_hens():
        end_production()
        return True

    # 2. 第1次 上一个 -> 陶瓷
    if not last_area(): return end_production()
    if not handle_ceramics(): return end_production()

    # 3. 第2次 上一个 -> 土料
    if not last_area(): return end_production()
    if not handle_clay(): return end_production()

    # 4. 第3次 上一个 -> 玩具
    if not last_area(): return end_production()
    if not handle_toys(): return end_production()

    # 5. 第4次 上一个 -> 编织
    if not last_area(): return end_production()
    if not handle_weaving(): return end_production()

    # 6. 第5次 上一个 -> 糕坊
    if not last_area(): return end_production()
    if not handle_pastry(): return end_production()

    # 7. 第6次 上一个 -> 木工
    if not last_area(): return end_production()
    if not handle_carpentry(): return end_production()

    # 8. 第7次 上一个 -> 豆腐加工
    if not last_area(): return end_production()
    if not handle_tofu(): return end_production()

    # 9. 第8次 上一个 -> 腌制
    if not last_area(): return end_production()
    if not handle_pickling(): return end_production()

    # 10. 第9次 上一个 -> 饼坊
    if not last_area(): return end_production()
    if not handle_pie(): return end_production()

    # 11. 第10次 上一个 -> 制糖
    if not last_area(): return end_production()
    if not handle_sugar(): return end_production()

    # 12. 第11次 上一个 -> 铡刀
    if not last_area(): return end_production()
    if not handle_chopper(): return end_production()

    # 13. 第12次 上一个 -> 豆坊
    if not last_area(): return end_production()
    if not handle_beans(): return end_production()

    # 14. 第13次 上一个 -> 石磨
    if not last_area(): return end_production()
    if not handle_stone_mill(): return end_production()

    # 15. 第14次 上一个 -> 鸡舍
    if not last_area(): return end_production()
    if not handle_chicken_coop(): return end_production()

    # 16. 退出界面
    if not exit_interface(): 
        end_production()
        return True

    end_production()
    return True

if __name__ == "__main__":
    handle_chicken_coop()