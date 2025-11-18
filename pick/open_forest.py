from pick.pick_utils import *
def open_forest():
    print("打开伐木林")
    zoom_and_locate()
    time.sleep(eval(os.environ.get("small_delay")))
    drag_ratio(0.7, 0.5, 0.3, 0.5)
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.8692,0.1937)
    time.sleep(eval(os.environ.get("small_delay")))
    return True
if __name__ == "__main__":
    open_forest()
    print(1)