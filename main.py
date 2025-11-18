from config import *
def start():
    print("开始流程")
    return True


from farming.farming import farming

from pick.pick import pick

from production.production import production

from sale.sale import sale

def main():
    # Start
    if not start():
        return

    while True:
        # 种地
        if not farming():
            break
        # 采集
        if not pick():
            break

        # 生产
        if not production():
            break

        # 清仓大甩卖
        if not sale():
            break

        # 回到“种地”
        # 循环继续运行

    print("流程结束")


if __name__ == "__main__":
    main()
