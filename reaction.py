import time


def get_app_name():
    pass


def get_app_index():
    name = get_app_name()
    if "照片" in name:
        return 1
    elif "PowerPoint" in name:
        return 2
    else:
        print("未在支持程序内执行手势")
        return 99


def catch():
    print('Done：抓取')


def tap():
    print('Done：点击')


def rotate(app_index: int):
    if app_index == 1:
        pass
    print('Done：旋转')


def move(app_index: int):
    if app_index == 1 or app_index == 2:
        pass
    print('Done：平移')


def zoom(app_index: int, signal: str):
    if app_index == 1:
        pass
    elif app_index == 2:
        pass
    print('Done：', "缩放" if signal == '-' else "放大")


def screenshot():
    pass
    print("Done：截图")


class Reaction:
    def __init__(self):
        pass

    def react(self, target: str):
        appIndex = get_app_index()
        if target == "点击":
            tap()
        elif target == "平移":
            move(appIndex)
        elif target == "旋转":
            rotate(appIndex)
        elif target == "抓取":
            catch()
        elif target == "缩放":
            zoom(appIndex, '-')
        elif target == "放大":
            zoom(appIndex, '+')
        elif target == "截图":
            screenshot()
        else:
            print("未添加此动作")


if __name__ == '__main__':
    time.sleep(3)
    react = Reaction()
    react.react("放大")

