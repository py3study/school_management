# -*- coding: utf-8 -
class Prompt(object):  # 提示信息显示
    colour_list = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'purple_red': 35,
        'bluish_blue': 36,
        'white': 37,
    }

    def __init__(self):
        pass

    @staticmethod
    def display(msg, colour='white'):
        choice = Prompt.colour_list.get(colour)
        #print(choice)
        if choice:
            info = "\033[1;{};1m{}\033[0m".format(choice,msg)
            return info
        else:
            return False


if __name__ == '__main__':
    pass
    # ret = Prompt.display('方法是否是地方撒地方','white')
    # print(ret)
