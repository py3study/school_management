from core.Course import Course
from core.Classes import Classes
#from core.Personal import Personal
from conf import settings
from lib.mypickle import MyPickle
from core.Prompt import Prompt

class Student(object):
    operate_lst = [
        ('查看课程', 'get_course'),
        ('查看班级', 'get_classes'),
        ('退出', 'q'),
    ]

    def __init__(self, info, name, age, sex, course, score, classes):
        self.info = info
        self.name = name
        self.age = age
        self.sex = sex
        self.course = course
        self.score = score
        self.classes = classes

        if self.info['role'] == 'Student':
            self.main()
        else:
            print('身份非法!')

    def main(self):
        #print('您好: {} 同学 欢迎使用校园后台管理系统!\n'.format(self.name))
        print(Prompt.display('您好: {} 同学 欢迎使用校园后台管理系统!\n'.format(self.info['username']), 'purple_red'))

    def q(self):
        exit()

    @staticmethod
    def student_all():  # 查看所有学生详细信息,返回生成器
        return MyPickle(settings.file_name['student']).load()

    def get_course(self):  # 查看课程
        # 调用课程方法
        ret = Course.get_course(self.course, self.info['role'])
        if ret:
            print('您的学习课程为: {}'.format(ret[0]['name']))
        else:
            print('未找到您的学习课程')

    def get_classes(self):  # 查看班级
        # 调用班级方法
        ret = Classes.get_classes(self.classes, self.info['role'])

        if ret:
            print('您所在的班级为: {}'.format(ret[0]['name']))
        else:
            print('未找到您所在的班级')

    @staticmethod
    def student_info():  # 查看所有学生名列表,比如['zhangsan','lisi']
        student_list = []
        for i in Student.student_all():
            student_list.append(i['name'])
        return student_list


if __name__ == '__main__':
    pass
