#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description:
@Author: Zpp
@Date: 2020-02-19 19:45:33
@LastEditTime: 2020-03-24 15:38:18
@LastEditors: Zpp
'''
from models.base import db
from models.system import Admin, Role, Route, Menu, Interface, InitSql, Folder
from conf.setting import Config, init_route, init_menu, sql_dir
import uuid
import datetime
import random
import copy
import os
import time


class BaseModel():
    def CreateDropRequest(self, isInit, params=None):
        s = db.session()
        try:
            db.drop_all()
            db.create_all()
            s.add(InitSql(isInit=False))
            s.commit()

            role_id = uuid.uuid4()
            role = Role(
                role_id=role_id, 
                name=u'超级管理员',
                mark=u'SYS_ADMIN'
            )
            s.add(role)
            s.commit()

            password = self.__get_code()
            if not isInit:
                admin = Admin(
                    admin_id=uuid.uuid4(),
                    username=u'Admin',
                    password=Config().get_md5(password),
                    avatarUrl='',
                    role_id=role_id
                )
            else:
                admin = Admin(
                    admin_id=params['admin_id'],
                    username=u'Admin',
                    password=params['password'],
                    avatarUrl='',
                    role_id=role_id
                )
            s.add(admin)
            s.commit()

            self.__init_routes(init_route, '0')
            self.__init_menus(init_menu, '0')

            folder = Folder(
                folder_id=uuid.uuid4(),
                admin_id=None,
                name=u'系统文件',
                is_sys=True
            )
            s.add(folder)
            s.commit()

            sql = s.query(InitSql).first()
            sql.isInit = True
            s.commit()
            return {
                'username': 'Admin',
                'password': password
            }
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def __get_code(self):
        code_list = []
        for i in range(10):   # 0~9
            code_list.append(str(i))
        for i in range(65, 91):  # A-Z
            code_list.append(chr(i))
        for i in range(97, 123):  # a-z
            code_list.append(chr(i))
        code = random.sample(code_list, 6)  # 随机取6位数
        code_num = ''.join(code)
        return code_num

    def __init_routes(self, data, pid):
        s = db.session()
        for r in data:
            route_id = uuid.uuid4()
            route = self.__create_route(r, route_id, pid)
            s.add(route)
            s.commit()
            if r.has_key('children'):
                self.__init_routes(r['children'], route_id)

    def __init_menus(self, data, pid):
        s = db.session()
        for m in data:
            menu_id = uuid.uuid4()
            menu = self.__create_menu(m, menu_id, pid)

            if m.has_key('interface'):
                interfaces = []
                for f in m['interface']:
                    interface = self.__create_interface(f, uuid.uuid4(), menu_id)
                    s.add(interface)
                    interfaces.append(interface)
                menu.interfaces = interfaces

            s.add(menu)
            s.commit()
            if m.has_key('children'):
                self.__init_menus(m['children'], menu_id)

    def __create_route(self, params, route_id, pid):
        return Route(
            route_id=route_id,
            pid=pid,
            name=params['name'],
            title=params['title'],
            path=params['path'],
            component=params['component'],
            componentPath=params['componentPath'],
            cache=params['cache']
        )

    def __create_menu(self, params, menu_id, pid):
        return Menu(
            menu_id=menu_id,
            pid=pid,
            title=params['title'],
            path=params['path'],
            icon=params['icon'],
            mark=params['mark']
        )

    def __create_interface(self, params, interface_id, menu_id):
        return Interface(
            menu_id=menu_id,
            interface_id=interface_id,
            name=params['name'],
            path=params['path'],
            method=params['method'],
            description=params['description'],
            mark=params['mark'],
            not_allow=params['not_allow']
        )

    def ExportSql(self, type = 1):
        try:
            config = Config()
            if not os.path.exists(sql_dir):
                os.mkdir(sql_dir)

            os.chdir(sql_dir)
            filename = 'TABLE%s.sql' % int(time.time() * 1000)
            
            sqlfromat = "%s -h%s -u%s -p%s -P%s %s >%s"
            if type == 2:
                sqlfromat = "%s -h%s -u%s -p%s -P%s -d %s >%s" # 不包含数据
            if type == 3:
                sqlfromat = "%s -h%s -u%s -p%s -P%s -t %s >%s" # 不包含表结构

            sql = (sqlfromat % ('mysqldump ',
                                config.host,
                                config.admin,
                                config.password,
                                config.port,
                                config.db,
                                filename))
            os.system(sql)
            return {
                'path': os.path.join(sql_dir, filename),
                'name': filename
            }
        except Exception as e:
            print e
            return str(e.message)

    def ImportSql(self, file):
        s = db.session()
        try:
            filename = 'TABLE%s.sql' % int(time.time() * 1000)
            config = Config()

            if not os.path.exists(sql_dir):
                os.mkdir(sql_dir)
            
            file_path = os.path.join(sql_dir, filename)
            file.save(file_path)
            
            sqlfromat = "%s -h%s -u%s -p%s -P%s %s <%s"
            sql = (sqlfromat % ('mysql ',
                                config.host,
                                config.admin,
                                config.password,
                                config.port,
                                config.db,
                                file_path))

            db.drop_all()
            os.system(sql)
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)
