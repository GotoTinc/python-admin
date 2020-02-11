#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 权限控制器
@Author: Zpp
@Date: 2019-09-10 16:01:46
@LastEditTime : 2020-02-11 14:52:29
@LastEditors  : Please set LastEditors
'''
from flask import request
from models.base import db
from models.system import Role, Route, Menu
from sqlalchemy import text
import uuid
import json


class RoleModel():
    def CreateRoleRequest(self, params):
        '''
        新建权限
        '''
        s = db.session()
        try:
            route = s.query(Route).filter(Route.route_id.in_(params['route_id'])).all()
            menu = s.query(Menu).filter(Menu.menu_id.in_(params['menu_id'])).all()

            item = Role(
                name=params['name'],
                role_id=uuid.uuid4(),
                checkKey=params['checkKey'],
                routes=route,
                menus=menu
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

    def ModifyRoleRequest(self, role_id, params):
        '''
        修改权限信息
        '''
        s = db.session()
        try:
            role = s.query(Role).filter(Role.role_id == role_id).first()
            if not role:
                return str('数据不存在')

            route = s.query(Route).filter(Route.route_id.in_(params['route_id'])).all()
            menu = s.query(Menu).filter(Menu.menu_id.in_(params['menu_id'])).all()

            role.name = params['name']
            role.checkKey = params['checkKey']
            role.routes = route
            role.menus = menu
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def LockRoleRequest(self, role_id, isLock):
        '''
        禁用权限
        '''
        s = db.session()
        try:
            s.query(Role).filter(Role.role_id.in_(role_id)).update({Role.isLock: isLock})
            s.commit()
            return True
        except Exception as e:
            print e
            s.rollback()
            return str(e.message)

    def QueryRoleByParamRequest(self, params):
        '''
        权限列表
        '''
        s = db.session()
        try:
            data = {}
            if params.has_key('is_disabled'):
                data['is_disabled'] = params['is_disabled']

            result = Role.query.filter_by(**data).order_by(Role.id).all()

            data = []
            for value in result:
                data.append(value.to_json())

            return data
        except Exception as e:
            print e
            return str(e.message)
