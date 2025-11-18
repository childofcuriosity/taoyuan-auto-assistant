def start_farm():
    print("【种地】开始")
    return True

from farming.check_status import check_status


from farming.harvest import harvest

from farming.decide_plant import decide_plant

from farming.plant_action import plant_action


def end_farm():
    print("【种地】结束")
    return True


def farming():
    """
    farming 主流程 = 流程图：
        start_farm → check_status
        check_status == 等待 → end
        check_status == 可收获 → harvest → decide_plant → 播种或结束
    """
    if not start_farm():
        return True
    status = check_status()

    if status == "growing":
        end_farm()
        return True

    elif status == "harvest" or status == "empty":
        if status == "harvest":
            if not harvest():
                end_farm()
                return True
        need = decide_plant()

        if need == "无":
            end_farm()
            return True

        # need 为作物名称
        plant_action(seed_type=need)
        end_farm()
        return True


    else:
        print("【种地】未知状态，直接结束")
        end_farm()
        return True
