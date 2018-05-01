from conf import settings
from lib.mypickle import MyPickle


class Classes(object):  # 班级
    def __init__(self, role, name, course, teacher):
        self.role = role  # 角色信息
        self.name = name  # 班级名
        self.course = course  # 课程
        self.teacher = teacher  # 讲师

    @staticmethod
    def classes_all():  # 查看所有班级,返回生成器
        return MyPickle(settings.file_name['classes']).load()

    @staticmethod
    def get_classes(classes, role):  # 查看登录用户对应的班级
        if not classes or not role:
            return '班级和角色不能为空!'
        classes_list = []
        # classes_all = MyPickle(settings.file_name['classes']).load()
        for i in Classes.classes_all():
            if role == 'Manager':  # 管理员查看所有
                classes_list.append(i)
            elif role == 'Student':  # 学生只能查看自己
                if classes == i['name']:
                    classes_list.append(i)
            elif role == 'Teacher':  # 老师只能查看自己
                if classes == i['teacher']:
                    classes_list.append(i)
                    # return classes_list
            else:
                return '角色未定义!'

        return classes_list

    @staticmethod
    def classes_exist(classes):  # 判断班级是否存在
        '''
        :param classes: 班级
        :return: True 可用(班级不存在) False 不可用(班级已存在)
        '''
        if classes == '':
            print('班级不能为空!')
            return False

        for i in Classes.classes_all():
            if classes == i['name']:
                # 当找到匹配时,return False
                return False
        return True


if __name__ == '__main__':
    pass
    # role = Manager
    ret = Classes.get_classes('fds', 'Manager')
    print(ret)
