import sys
from conf import settings
from core import Login
from core.Personal import Personal
from core.Manager import Manager
from core.Teacher import Teacher
from core.Student import Student
from core.Prompt import Prompt


def main():
    ret = Login.Login().login()  # 执行登录程序
    if ret:
        clas = getattr(sys.modules['core.' + ret['role']], ret['role'])  # 根据角色名获取类名(角色名和类名一致)
        if ret['role'] == 'Manager':  # 判断角色为管理员
            obj = clas(ret)  # 实例化,ret返回格式如下{'username': 'xiao', 'role': 'Manager'}
        elif ret['role'] == 'Teacher':  # 判断角色为老师
            info = Personal.get_info(ret)  # 获取当前登录用户的详细信息
            obj = clas(ret, info['name'], info['age'], info['sex'], info['course'])  # 实例化对象
        elif ret['role'] == 'Student':
            info = Personal.get_info(ret)
            obj = clas(ret, info['name'], info['age'], info['sex'], info['course'], info['score'],
                       info['classes'])
        else:
            print('角色未定义!')

        while True:
            # for key, item in enumerate(clas.operate_lst, 1):  # 获取每个角色类的operate_lst静态属性,显示的序列号从1开始
            #     print(str(key)+'.', item[0])
            interlacing_color(clas.operate_lst)
            num = input('输入您要做的操作序号：').strip()
            if num.isdigit():  # 判断数字
                num = int(num)  # 转换数字类型
                if num in range(1, len(clas.operate_lst) + 1):  # 判断输入的序号范围
                    if hasattr(obj, clas.operate_lst[num - 1][1]):  # 判断序号对应的类方法,是否存在
                        getattr(obj, clas.operate_lst[num - 1][1])()  # 执行对应的方法
                    else:
                        print('序号对应的方法未定义!')
                else:
                    print('序号不存在,请重新输入!')
            else:
                print('操作序号必须为数字!')


def interlacing_color(operate_lst):  # 隔行换色
    diff = 0  # 差值
    if len(operate_lst) > len(Prompt.colour_list):  # 当菜单列表长度大于颜色列表长度时
        diff = len(operate_lst) - len(Prompt.colour_list)  # 菜单列表长度-颜色列表长度

    colour_list = list(Prompt.colour_list)
    new_list = colour_list  # 新的颜色列表

    if diff >= 0:  # 当菜单列表长度大于等于颜色列表长度时
        for i in range(diff + 1):
            new_list.append(colour_list[i])  # 添加颜色,使颜色列表等于菜单列表长度

    count = -1  # 颜色列表索引值，默认为-1
    for key, item in enumerate(operate_lst, 1):  # 获取每个角色类的operate_lst静态属性,显示的序列号从1开始
        count += 1  # 索引加1
        ret = Prompt.display('{}.\t{}'.format(key, item[0]), new_list[count])  # 按照列表顺序显示颜色
        print(ret)
