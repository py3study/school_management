import os
from conf import settings
from core.Course import Course
from core.Classes import Classes
from core.Personal import Personal
from core.Student import Student
from lib.mypickle import MyPickle
from lib.mylogger import Logger
from core.Prompt import Prompt


class Teacher(object):
    operate_lst = [
        ('查看课程', 'see_course'),
        ('查看班级', 'see_classes'),
        ('查看学员信息', 'see_student'),
        ('修改学员成绩', 'manage_classes'),
        ('退出', 'q'),
    ]

    def __init__(self, info, name, age, sex, course):
        self.info = info
        self.name = name
        self.age = age
        self.sex = sex
        self.course = course
        if self.info['role'] == 'Teacher':
            self.main()
        else:
            print('身份非法!')

    def main(self):
        print(Prompt.display('您好: {} 老师 欢迎使用校园后台管理系统!\n'.format(self.info['username']), 'purple_red'))

    def q(self):
        exit()

    @staticmethod
    def teacher_all():
        return MyPickle(settings.file_name['teacher']).load()

    @staticmethod
    def teacher_info():  # 查看所有老师详细信息
        teacher_list = []
        for i in Teacher.teacher_all():
            teacher_list.append(i)
        return teacher_list

    def see_course(self):  # 查看老师对应的课程
        ret = Course.get_course(self.course, self.info['role'])

        if ret:
            print('当前教学的课程为:'.center(45, '='))
            for k, v in enumerate(ret, 1):
                print('{}.\t{}'.format(k, v['name']))
            print(''.center(53, '='))
        else:
            print('没有找到您的教学课程!')

    def classes_info(self):  # 查看老师对应的班级,返回列表
        ret = Classes.get_classes(self.name, self.info['role'])
        classes_list = []
        if ret:
            for i in ret:
                classes_list.append(i)
                return classes_list
        else:
            return classes_list

    def see_classes(self):  # 查看老师对应的班级
        ret = self.classes_info()
        if ret:
            print('当前教学的班级为:'.center(45, '='))
            for k, v in enumerate(ret, 1):
                print('{}.\t{}'.format(k, v['name']))
            print(''.center(53, '='))
        else:
            print('没有找到您的教学班级!')

    def see_student(self):  # 查看班级学员信息
        ret = self.student_info(self.classes_info()[0]['name'])
        if ret:
            print('当前教学班级学员信息列表如下:'.center(45, '='))
            for k, v in enumerate(ret, 1):
                print('{}.\t姓名:{} 性别:{} 年龄:{} 成绩:{} 班级:{} 课程:{}'.format(k, v['name'], v['sex'],
                                                                        v['age'], v['score'],
                                                                        v['classes'], v['course']))
            print(''.center(53, '='))
        else:
            print('教学班级的学员列表为空!')

    def student_info(self, classes):  # 查看班级对应的学生列表
        student_list = []
        for i in Student.student_all():
            if classes == i['classes']:
                student_list.append(i)
        return student_list

    def modify_score(self, student, score):  # 修改学生成绩
        if not score:
            print('学生名不能为空!')
            return False

        student_list = []
        for i in Student.student_all():
            if student == i['name']:
                # 修改成绩
                i['score'] = score
            # 写入列表
            student_list.append(i)

        return student_list

    @staticmethod
    def rewrite(student_list):
        if not student_list:
            return '学生列表不能为空!'

        os.remove(settings.file_name['student'])  # 删除原有文件
        # 重新写入文件
        for i in student_list:
            ret = Personal.write_user_details(i, 'student')
            if ret is False:
                return False
        return True

    def manage_classes(self):  # 修改班级学员成绩
        classes_list = self.classes_info()
        if classes_list == []:
            print('当前没有教学班级!')
        else:
            while True:
                print('当前管理的班级为:')
                for k, v in enumerate(classes_list, 1):
                    print('{}.\t{}'.format(k, v['name']))
                classes_id = input('请输入班级编号,或输入b返回菜单 ').strip()
                if classes_id.upper() == 'B':
                    break
                if classes_id.isdigit():
                    classes_id = int(classes_id)
                    if classes_id in range(1, len(classes_list) + 1):
                        classes = classes_list[classes_id - 1]['name']
                        student_list = self.student_info(classes)
                        if student_list == []:
                            print('当前班级没有学生!')
                            continue
                        else:
                            print('===================================')
                            print('{} 班级学员列表如下:'.format(classes))
                            for k, v in enumerate(student_list):
                                print('{}.\t姓名:{} 性别:{} 年龄:{} 成绩:{} 班级:{} 课程:{}'.format(k + 1, v['name'], v['sex'],
                                                                                        v['age'], v['score'],
                                                                                        v['classes'], v['course']))
                            student_id = input('请输入学生编号: ').strip()
                            if student_id.isdigit():
                                student_id = int(student_id)
                                if student_id in range(1, len(student_list) + 1):
                                    student = student_list[student_id - 1]
                                    score = input('请输入要修改的成绩: ').strip()
                                    if score.isdigit():
                                        score = int(score)
                                        if score in range(1, 101):
                                            # 修改成绩
                                            ret = self.modify_score(student['name'], score)
                                            ret1 = self.rewrite(ret)
                                            # print(ret)
                                            if ret1:
                                                Logger.logger.info('%s 修改了%s学生成绩' % (self.info['username'], student['name']))  # 记录日志
                                                print(Prompt.display('修改成绩成功!', 'green'))
                                                break
                                            else:
                                                print('修改失败!')
                                                continue
                                        else:
                                            print('成绩不能大于100!')
                                            continue
                                    else:
                                        print('成绩请输入数字!')
                                        continue
                                else:
                                    print('学生编号超出范围,请重新输入！')
                                    continue
                            else:
                                print('学生编号输入错误!')
                                continue
                    else:
                        print('班级编号超出范围,请重新输入!')
                        continue
                else:
                    print('班级编号输入错误,请重新输入!')
                    continue


if __name__ == '__main__':
    pass