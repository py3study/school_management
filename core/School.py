from conf import settings
from lib.mypickle import MyPickle

class School(object):  # 班级
    def __init__(self):pass

    @staticmethod
    def school_all():  # 查看所有学校,返回生成器
        return MyPickle(settings.file_name['school']).load()

    @staticmethod
    def school_info():  # 查看所有学校列表,比如['北京','上海']
        school_list = []
        for i in School.school_all():
            school_list.append(i['name'])
        return school_list

    @staticmethod
    def school_exist(name):  # 判断学校名是否存在
        '''
        #判断学校名是否可用
        :param username: 学校名
        :return: True 可用(不存在) False 不可用(已存在)
        '''
        if not name:
            print('学校名不能为空!')
            return False
        user = MyPickle(settings.file_name['school']).load()
        for i in user:
            if name == i['name']:
                return False
        return True

    @staticmethod
    def write_school(information):
        '''
        写入学校信息文件
        :param information: 学校名,数据类型为字典
        :return: True 成功 False 失败
        '''
        if not information:
            return '学校名不能为空!'

        school = MyPickle(settings.file_name['school'])
        ret = school.dump(information)
        if ret:
            return True
        else:
            return False