# -*- coding: utf-8 -*-
# 自动创建settings模块中的所有txt文件
# 不存在则创建,否则不创建

import os
from conf import settings
from core.Login import get_pwd
from lib.mypickle import MyPickle

files = settings.file_name  # 获取文件字典
for i in files:  # 遍历字典
    if os.path.exists(settings.file_name[i]) is False:  # 判断文件是否存在，False表示不存在
        #print(settings.file_name[i])
        with open(settings.file_name[i], mode='ab') as mk:  # 打开每一个文件
            if i == 'user':  # 判断是否为用户认证文件
                # 写入默认的用户认证文件
                first_man = {'username': 'xiao', 'password': '123'}  # 默认管理员
                encrypt_pwd = get_pwd(first_man['username'], first_man['password'])  # 获取加密密码
                info = {'username': first_man['username'], 'password': encrypt_pwd, 'role': 'Manager'}  # 组合字典
                MyPickle(files[i]).dump(info)  # 写入一条字典
            elif i == 'course':
                # 课程信息写入默认内容
                course_default = [
                    {'name': 'linux', 'cycle': 3, 'price': 7000, 'city': '北京'},
                    {'name': 'python', 'cycle': 5, 'price': 20000, 'city': '北京'},
                    {'name': 'go', 'cycle': 7, 'price': 22000, 'city': '上海'},
                ]
                for j in course_default:
                    MyPickle(files[i]).dump(j)  # 写入3条课程信息
            elif i == 'school':
                school_default = [
                    {'name':'北京'},
                    {'name':'上海'},
                ]
                for s in school_default:
                    MyPickle(files[i]).dump(s)  # 写入2条学校信息

