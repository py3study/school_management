from conf import settings
from core.Course import Course
from core.Classes import Classes
from core.Teacher import Teacher
from core.Student import Student
from core.School import School
from core.Personal import Personal
from core.Login import get_pwd
from lib.mypickle import MyPickle
from lib.mylogger import Logger
from core.Prompt import Prompt


class Manager(object):  # 管理员后台
    operate_lst = [
        ('创建老师', 'create_teacher'),
        ('创建班级', 'create_classes'),
        ('创建课程', 'create_course'),
        ('创建学生', 'create_student'),
        ('创建学校', 'create_school'),
        ('查看老师', 'ses_teacher'),
        ('查看班级', 'ses_classes'),
        ('查看课程', 'ses_course'),
        ('查看学生', 'ses_student'),
        ('查看学校', 'ses_school'),
        ('退出', 'q')
    ]

    def __init__(self, info):
        # 用户信息
        self.info = info

        # 判断用户角色
        if info['role'] == 'Manager':
            self.main()
        else:
            print('身份非法!')

    def main(self):
        print(Prompt.display('您好: {} 管理员 欢迎使用校园后台管理系统!\n'.format(self.info['username']), 'purple_red'))

    def q(self):  # 退出
        exit()

    def create_teacher(self):  # 创建老师
        while True:
            name = self.input_check('老师的姓名')
            # 执行方法,判断用户名是否存在
            ret = Personal.username_exist(name)
            if ret is False:
                print('用户已存在，请重新输入!')
                continue

            pwd = self.input_check('老师的密码')
            sex = self.input_check('老师的性别(M男|F女)', 'sex')
            sex = sex.upper()
            age = self.input_check('老师的年龄', 'int', 256)
            # 执行方法，执行选择课程操作
            course = self.choice_courses()

            # 获取加密的密码
            password = get_pwd(name, pwd)

            ret1 = Personal.write_auth_file(name, password, 'Teacher')
            if ret1:
                # 写入老师详细信息文件
                t1_info = {'name': name, 'sex': sex, 'age': age, 'course': course}
                ret2 = Personal.write_user_details(t1_info, 'teacher')

                if ret2:
                    Logger.logger.info('%s 创建了%s老师' % (self.info['username'],name))  # 记录日志
                    print(Prompt.display('添加成功!信息为:', 'green'))
                    print('姓名:{} 性别:{} 年龄:{} 课程:{}'.format(name, sex, age, course))
                    break
                else:
                    print('写入老师详细信息失败!')
                    continue

            else:
                print('写入用户注册文件失败!')
                continue

    def create_classes(self):  # 创建班级
        while True:
            classes = self.input_check('班级名')
            # 执行方法，判断班级名是否存在
            ret = Classes.classes_exist(classes)
            if ret is False:
                print('班级名已经存在，请重新输入!')
                continue
            # 执行方法，执行选择课程信息
            course = self.choice_courses()
            # 查看课程对应的老师列表
            teacher_list = Course.course_teacher(course)
            if teacher_list == []:
                print('当前课程没有老师，请创建老师')
                continue
            else:
                print('当前课程对应的老师如下:')
                for k, v in enumerate(teacher_list):
                    print(str(k + 1) + '. ', v)
                teacher_id = input('请输入老师的编号: ').strip()
                if teacher_id.isdigit():
                    teacher_id = int(teacher_id)
                    if teacher_id in range(len(teacher_list) + 1):

                        # 写入班级详细信息
                        classes_f = MyPickle(settings.file_name['classes'])
                        try:
                            t1_classes = {'name': classes, 'course': course, 'teacher': teacher_list[teacher_id - 1]}

                            classes_f.dump(t1_classes)
                            Logger.logger.info('%s 创建了%s班级' % (self.info['username'], classes))  # 记录日志
                            print(Prompt.display('添加班级成功!信息为:', 'green'))
                            print('名字: {} 课程: {} 老师: {}'.format(classes, course, teacher_list[teacher_id - 1]))
                            break
                        except Exception:
                            print('添加班级失败!')
                            continue
                else:
                    print('输入老师的编号不正确,请重新输入!')
                    continue

    def create_course(self):  # 创建课程
        while True:
            course = self.input_check('课程名')
            # 执行方法，判断课程名是否存在
            ret = Course.course_exist(course)
            if ret is False:
                print('课程名已经存在，请重新输入!')
                continue

            cycle = self.input_check('周期(单位:月)', 'int', 36)
            price = self.input_check('价格(单位:人民币)', 'int', 1000000)
            self.ses_school()  # 显示学校列表
            school_list = School.school_info()
            city_id = self.input_check('学校编号', 'int', len(school_list)+1)
            city = school_list[int(city_id) - 1]
            # 写入课程详细信息
            course_f = MyPickle(settings.file_name['course'])
            try:
                t1_course = {'name': course, 'cycle': cycle, 'price': price, 'city': city}

                course_f.dump(t1_course)
                Logger.logger.info('%s 创建了%s课程' % (self.info['username'], course))  # 记录日志
                print(Prompt.display('添加课程成功!信息为:', 'green'))
                print('课程: {} 周期: {}个月 价格: ￥{} 城市: {}'.format(course, cycle, price, city))
                break
            except Exception:
                print('添加课程失败!')
                continue

    def create_student(self):  # 创建学生
        while True:
            name = self.input_check('学生的姓名')
            # 执行方法,判断用户名是否存在
            ret = Personal.username_exist(name)
            if ret == False:
                print('用户已存在，请重新输入!')
                continue

            pwd = self.input_check('学生的密码')
            sex = self.input_check('学生的性别(M男|F女)', 'sex')
            sex = sex.upper()
            age = self.input_check('学生的年龄', 'int', 256)
            # 执行方法，执行选择课程信息
            course = self.choice_courses()
            # 执行方法，查看课程对应的班级
            classes_list = Course.course_classes(course)
            if classes_list == []:
                print('当前课程没有班级，请创建班级')
                continue
            print('当前课程对应的班级如下:')
            for k, v in enumerate(classes_list):
                print(str(k + 1) + '. ', v)
            classes_id = input('请输入班级编号: ').strip()
            if classes_id.isdigit():
                classes_id = int(classes_id)
                if classes_id in range(1, len(classes_list) + 1):
                    classes = classes_list[classes_id - 1]
            else:
                print('班级编号输入错误,请重新输入')
                continue

            # 写入登录文件
            password = get_pwd(name, pwd)
            ret1 = Personal.write_auth_file(name, password, 'Student')
            if ret1:
                # 写入学生详细信息文件
                s1_info = {'name': name, 'sex': sex, 'age': age, 'course': course, 'score': 0, 'classes': classes}
                ret2 = Personal.write_user_details(s1_info, 'student')
                if ret2:
                    Logger.logger.info('%s 创建了%s学生' % (self.info['username'], name))  # 记录日志
                    print(Prompt.display('添加成功!信息为:', 'green'))
                    print('姓名:{} 性别:{} 年龄:{} 课程:{} 成绩:0 班级:{}'.format(name, sex, age, course, classes))
                    break
                else:
                    print('写入学生详细信息失败!')
                    continue

            else:
                print('写入用户注册文件失败!')
                continue

    def create_school(self):
        while True:
            self.ses_school()
            name = self.input_check('新学校名')
            if name.isdigit():
                print(Prompt.display('学校名不能为数字!', 'red'))
                continue
            ret = School.school_exist(name)
            if ret is False:
                #print('学校名已存在，请重新输入!')
                print(Prompt.display('学校名已存在，请重新输入!', 'red'))
                continue
            s_info = {'name': name}
            ret2 = School.write_school(s_info)
            if ret2:
                Logger.logger.info('%s 创建了%s学校' % (self.info['username'], name))  # 记录日志
                print(Prompt.display('添加成功!信息为:', 'green'))
                print('学校名:{}'.format(name))
                break
            else:
                print(Prompt.display('写入学校细信息失败!', 'red'))
                continue


    def input_check(self, msg, data_type='str', scope=0, li=[]):  # 输出检测
        '''
        :param func: 返回主菜单方法，比如年龄
        :param msg: 提示信息，比如年龄
        :param data_type: 数据类型,模式是str
        :param scope: 如果为数字类型，不能超过这个数字，比如256
        :return: True 检测成功 False 检测失败
        '''
        def entry(msg):
            ret = input('请输入%s,或输入q退出: ' % msg).strip()
            return ret

        s1 = entry(msg)
        li.append(s1)

        if not s1:
            print('%s不能为空!' % msg)
            self.input_check(msg, data_type, scope)
        else:
            if s1.upper() == 'Q':
                self.q()
                return False
            else:
                if data_type == 'int':
                    if s1.isdigit():
                        s1 = int(s1)
                        if s1 == 0:
                            print('%s不能小于 %s!' % (msg, 0))
                            self.input_check(msg, data_type, scope)
                        if s1 >= scope:
                            print('%s不能超过 %s!' % (msg, scope))
                            self.input_check(msg, data_type, scope)
                        else:
                            return li[-1]
                    else:
                        print('%s请输入整数!' % msg)
                        self.input_check(msg, data_type, scope)
                elif data_type == 'sex':
                    if s1 == '':
                        print('性别不能为空!')
                        self.input_check(msg, data_type, scope)
                    elif s1.upper() == 'M' or s1.upper() == 'F':
                        return li[-1]
                    else:
                        print('性别请输入M或者F')
                        self.input_check(msg, data_type, scope)

                return li[-1]

    def choice_courses(self):  # 选择课程操作
        while True:
            print('选择课程: ')
            course_info = Course.course_info()
            # print(course_info)
            for k, v in enumerate(course_info):
                print(str(k + 1) + '. ', v)
            # exit()
            course_id = input('请输入课程编号: ').strip()
            if course_id.isdigit():
                course_id = int(course_id)
                if course_id in range(1, len(course_info) + 1):
                    course = course_info[course_id - 1]
                    return course
                else:
                    print('课程编号超出范围,请重新输入!')
                    continue
            else:
                print('课程编号输入错误,请重新输入!')
                continue

    def ses_teacher(self):  # 查看所有老师
        teacher_list = Teacher.teacher_info()

        if not teacher_list:
            print('当前所有老师列表为空!')
        else:
            print('当前所有老师列表如下:'.center(30, '='))

            for k, v in enumerate(teacher_list):
                print('{}.\t姓名:{} 性别:{} 年龄:{} 课程:{}'.format(k + 1, v['name'], v['sex'], v['age'], v['course']))
            print(''.center(38, '='))

    def ses_classes(self):  # 查看所有班级
        student_list = Classes.get_classes('linux', 'Manager')
        if not student_list:
            print('当前所有班级列表为空!')
        else:
            print('当前所有班级列表如下:'.center(30, '='))
            for k, v in enumerate(student_list):
                print('{}.\t名字:{} 课程:{} 老师:{}'.format(k + 1, v['name'], v['course'], v['teacher']))
            print(''.center(38, '='))

    def ses_course(self):  # 查看所有课程
        course_list = Course.get_course('linux', self.info['role'])
        if not course_list:
            print('当前所有课程列表为空!')
        else:
            print('当前所有课程列表如下:'.center(30, '='))

            for k, v in enumerate(course_list):
                print('{}.\t名字:{} 周期:{} 价格:{} 城市:{} '.format(k + 1, v['name'], v['cycle'], v['price'], v['city']))
            print(''.center(38, '='))

    def ses_student(self):  # 查看所有学生
        student_list = []
        for i in Student.student_all():
            student_list.append(i)
        if not student_list:
            print('当前所有学生列表为空!')
        else:
            print('当前所有学生列表如下:'.center(45, '='))

            for k, v in enumerate(student_list):
                print(
                    '{}.\t姓名:{} 性别:{} 年龄:{} 成绩:{} 班级:{} 课程:{}'.format(k + 1, v['name'], v['sex'], v['age'], v['score'],
                                                                      v['classes'], v['course']))
            print(''.center(53, '='))

    def ses_school(self):  # 查看所有学校
        school_list = []
        for i in School.school_all():
            school_list.append(i)
        if not school_list:
            print('当前所有校区列表为空!')
        else:
            print('当前所有校区列表如下:'.center(30, '='))
            for k, v in enumerate(school_list):
                print(
                    '{}.\t{}'.format(k + 1, v['name']))
            print(''.center(35, '='))


if __name__ == '__main__':
    Manager({'username': 'xiao', 'role': 'Manager'})
