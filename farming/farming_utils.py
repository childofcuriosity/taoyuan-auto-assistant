from utils import *
# 作物顺序（左到右）
CROP_LIST = ["小麦", "大豆", "甘蔗", "水稻", "白菜", "辣椒", "土豆", "苎麻"]
def tap_field():
    print("点按田地")
    click_ratio(0.6900, 0.2544)  
    return True

def use4field(rx,ry):
    mouse_down_ratio(rx,ry)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.5067,0.5032)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.7223,0.3627)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.7603,0.3937)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.5344,0.5452)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.5879,0.5810)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.8031,0.4143)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.8411,0.4444)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.6299,0.6143)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.6665,0.6333)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.8893,0.4754)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.9375,0.5167)
    time.sleep(eval(os.environ.get("small_delay")))
    move_ratio(0.7205,0.6730)
    time.sleep(eval(os.environ.get("small_delay")))
    mouse_up_ratio()

