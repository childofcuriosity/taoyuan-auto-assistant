from utilsutils.windows_method import *
from utilsutils.vlm_method import *
import re
def zoom_and_locate():
    print("【查看】缩放最小并定位蒲公英")
    time.sleep(eval(os.environ.get("small_delay")))
    drag_ratio(0.5, 0.5, 0.6, 0.5)  
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.7881, 0.9361)
    time.sleep(eval(os.environ.get("small_delay")))
    ctrl_scroll_ratio(-200)  
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.4150, 0.9767)
    time.sleep(eval(os.environ.get("small_delay")))
    click_ratio(0.7166, 0.9361)
    time.sleep(eval(os.environ.get("big_delay")))
    click_ratio(0.0734, 0.1928)
    time.sleep(eval(os.environ.get("small_delay")))
    return True


def screenshot(image_path = "adb_screen.png"  ):
    print("截屏")
    adb_screenshot(image_path)
    return image_path


from PIL import Image

def create_white_image_like(input_path: str, output_path: str):
    """
    新建一个与 input_path 图像同尺寸的全白图片，并保存到 output_path
    """
    img = Image.open(input_path)
    white_img = Image.new("RGB", img.size, (255, 255, 255))  # 全白图
    white_img.save(output_path)



def copy_rectangle_by_ratio(rectangle_ratio, input1_path, input2_path, output_path):
    """
    将 input1 中 rectangle_ratio 比例区域复制到 input2 的对应位置，并保存为 output_path

    rectangle_ratio: (left_ratio, top_ratio, right_ratio, bottom_ratio)
    """
    img1 = Image.open(input1_path)
    img2 = Image.open(input2_path)

    assert img1.size == img2.size, "两张图片尺寸必须一致"

    w, h = img1.size

    left_ratio, top_ratio, right_ratio, bottom_ratio = rectangle_ratio

    # 计算真实像素区域
    left = int(w * left_ratio)
    top = int(h * top_ratio)
    right = int(w * right_ratio)
    bottom = int(h * bottom_ratio)

    # 裁剪 input1 区域
    region = img1.crop((left, top, right, bottom))

    # 把裁剪区域贴到 input2 的对应位置
    img2.paste(region, (left, top))

    # 保存结果
    img2.save(output_path)




if __name__ == "__main__":
    zoom_and_locate()
    print(1)