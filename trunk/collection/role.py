#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限控制器
@Author: Zpp
@Date: 2019-09-10 16:01:46
@LastEditTime: 2019-10-17 14:48:34
@LastEditors: Zpp
'''
from flask import request
from models.base import db
from models.system import Role, Route, Menu
import uuid


class RoleModel():
    def CreateRoleRequest(self, params):
        '''
        新建权限
        '''
        s = db.session()
        try:
            item = Role(
                name=params['name'],
                type=int(params['type']),
                role_id=uuid.uuid4
            )
            s.add(item)
            s.commit()
            return True
        except Exception as e:
            s.rollback()
            print e
            return str(e.message)

    def GetRoleRequest(self, role_id):
        '''
        查询权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            return role.to_json()
        except Exception as e:
            print e
            return str(e.message)

    def ModifyRoleToRoute(self, role_id, route_id):
        '''
        修改路由权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            route = []
            for key in route_id:
                item = s.query(Route).filter(Route.role_id == key).first()
                if item:
                    route.append(item)

            role.routes = route
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def ModifyRoleToMenu(self, role_id, menu_id):
        '''
        修改菜单权限
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            menu = []
            for key in menu_id:
                item = s.query(Menu).filter(Menu.menu_id == key).first()
                if item:
                    menu.append(item)

            role.menus = menu
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def ModifyRoleRequest(self, role_id, name):
        '''
        修改权限信息
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            role.name = name
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockRoleRequest(self, role_id):
        '''
        禁用权限
        '''
        s = db.session()
        try:
            for key in role_id:
                role = s.query(Role).filter(Role.role_id == key).first()
                if not role:
                    continue
                role.isLock = False
                s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def QueryRoleByParamRequest(self, params, page=1, page_size=20, order_by='id'):
        '''
        权限列表
        '''
        s = db.session()
        try:
            Int = ['isLock', 'type']
            data = {}

            for i in Int:
                if params.has_key(i):
                    data[i] = params[i]

            result = Route.query.filter_by(*data).filter(
                Route.name.like("%" + params['name'] + "%") if params.has_key('name') else ''
            ).order_by(order_by).paginate(page, page_size, error_out=False)

            data = []
            for value in result.items:
                data.append(value.to_json())

            return {'data': data, 'total': result.total}
        except Exception as e:
            print e
            return str(e.message)
