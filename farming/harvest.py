from farming.farming_utils import *
def harvest():
    print("【种地】执行收获")
    rx, ry = 0.4955,0.8206
    use4field(rx,ry)
    return True

if __name__ == "__main__":
    harvest()
    print(1)