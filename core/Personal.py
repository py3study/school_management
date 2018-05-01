# -*- coding: utf-8 -*-
from conf import settings
from lib.mypickle import MyPickle


class Personal(object):  # 获取个人信息

    def __init__(self):
        pass

    def get_info(self):  # 获取个人详细信息，返回字典
        role = self['role'].lower()  # 角色转换为小写
        user = MyPickle(settings.file_name[role]).load()
        for i in user:
            # print(i)
            if self['username'] == i['name']:
                return i
        return False

    @staticmethod
    def username_exist(username):  # 判断用户名是否存在
        '''
        #判断注册用户名是否可用
        :param username: 用户名
        :return: True 可用(用户不存在) False 不可用(用户已存在)
        '''
        if not username:
            print('用户名不能为空!')
            return False
        user = MyPickle(settings.file_name['user']).load()
        for i in user:
            if username == i['username']:
                return False
        return True

    @staticmethod
    def write_auth_file(username, password, role):
        '''
        写入用户认证文件
        :param username: 用户名
        :param password: 密码
        :param role: 角色
        :return: True 成功 False 失败
        '''
        t1_user = {'username': username, 'password': password, 'role': role}
        user = MyPickle(settings.file_name['user'])
        write_user = user.dump(t1_user)
        if write_user:
            return True
        else:
            return False

    @staticmethod
    def write_user_details(information, role):
        '''
        写入用户详细信息文件
        :param information: 用户详细信息,数据类型为字典
        :return: True 成功 False 失败
        '''
        if not information or not role:
            return '用户详细信息或者角色不能为空!'

        user = MyPickle(settings.file_name[role])
        write_user = user.dump(information)
        if write_user:
            return True
        else:
            return False


if __name__ == '__main__':
    pass
