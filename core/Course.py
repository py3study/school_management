from conf import settings
from lib.mypickle import MyPickle
from core.Classes import Classes


class Course(object):

    def __init__(self, role, name, cycle, price, city):
        self.role = role
        self.name = name
        self.cycle = cycle  # 周期
        self.price = price  # 价格
        self.city = city  # 城市

    @staticmethod
    def course_all():  # 查看所有课程详细信息，返回生成器
        return MyPickle(settings.file_name['course']).load()

    @staticmethod
    def get_course(course, role):  # 查看角色对应的课程详细信息
        if not course or not role:
            return '课程和角色不能为空!'
        course_list = []
        for i in Course.course_all():  # 遍历所有课程
            if role == 'Manager':  # 管理员查看所有
                course_list.append(i)
            elif role == 'Student':  # 学生只能查看自己
                if course == i['name']:
                    course_list.append(i)
                    # return course_list
            elif role == 'Teacher':  # 老师只能查看自己
                if course == i['name']:
                    course_list.append(i)
                    # return course_list
            else:
                return '角色未定义!'

        return course_list

    @staticmethod
    def course_exist(course):  # 判断课程是否存在
        '''
        :param course: 课程
        :return: True 可用(课程不存在) False 不可用(课程已存在)
        '''
        if course == '':
            print('课程不能为空!')
            return False
        for i in Course.course_all():  # 遍历所有课程
            # 判断用户名是否匹配
            if course == i['name']:
                # 当找到匹配时,return False
                return False
        return True

    @staticmethod
    def course_classes(course):  # 查看课程对应的班级
        if not course:
            print('课程不能为空!')
            return False

        course_list = []
        for i in Classes.classes_all():  # 遍历所有班级
            if course == i['course']:
                course_list.append(i['name'])
        return course_list

    @staticmethod
    def course_teacher(course):  # 查看课程对应的老师
        if not course:
            print('课程不能为空!')
            return False

        teacher_all = MyPickle(settings.file_name['teacher']).load()  # 遍历所有老师
        teacher = []
        for i in teacher_all:
            if course == i['course']:
                teacher.append(i['name'])
        return teacher

    @staticmethod
    def course_info():  # 查看课程名列表,比如['linux', 'python', 'go']
        course_list = []
        for i in Course.course_all():
            course_list.append(i['name'])
        return course_list


if __name__ == '__main__':
    pass
