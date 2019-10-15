#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 系统相关的几张表结构
@Author: Zpp
@Date: 2019-09-05 15:57:55
@LastEditTime: 2019-10-15 15:41:59
@LastEditors: Zpp
'''
from models.base import db
import datetime


class User(db.Model):
    '''
    用户
    '''
    __tablename__ = 'db_user'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    user_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    nickname = db.Column(db.String(64))
    sex = db.Column(db.SmallInteger, default=1)
    avatarUrl = db.Column(db.String(255))
    isLock = db.Column(db.Boolean, index=True, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('db_role.id'))
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    __table_args__ = ({"useexisting": True})

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        if "update_time" in dict:
            dict["update_time"] = dict["update_time"].strftime('%Y-%m-%d %H:%M:%S')
        if "create_time" in dict:
            dict["create_time"] = dict["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        return dict

    def __repr__(self):
        return '<User %r>' % self.username


MenuToRole = db.Table(
    'db_menu_to_role',
    db.Column('role_id', db.Integer, db.ForeignKey('db_role.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('db_menu.id'))
)


RouteToRole = db.Table(
    'db_route_to_role',
    db.Column('route_id', db.Integer, db.ForeignKey('db_route.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('db_role.id'))
)


class Role(db.Model):
    '''
    权限
    '''
    __tablename__ = 'db_role'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    role_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    type = db.Column(db.SmallInteger, index=True, default=1)
    isLock = db.Column(db.Boolean, index=True, default=True)
    users = db.relationship('User', backref='role')
    menus = db.relationship('Menu',
                            secondary=MenuToRole,
                            backref=db.backref('db_role', lazy='dynamic'),
                            lazy='dynamic')
    routes = db.relationship('Route',
                             secondary=RouteToRole,
                             backref=db.backref('db_route', lazy='dynamic'),
                             lazy='dynamic')
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Role %r>' % self.name


class Route(db.Model):
    '''
    路由
    '''
    __tablename__ = 'db_route'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    route_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    parentId = db.Column(db.String(36), nullable=False, index=True, default='0')
    name = db.Column(db.String(64), nullable=False, unique=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False)
    component = db.Column(db.String(255), nullable=False)
    componentPath = db.Column(db.String(255), nullable=False)
    cache = db.Column(db.Boolean, index=True, default=True)
    isLock = db.Column(db.Boolean, index=True, default=True)
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Route %r>' % self.name


class Menu(db.Model):
    '''
    菜单
    '''
    __tablename__ = 'db_menu'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    menu_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    parentId = db.Column(db.String(36), nullable=False, index=True, default='0')
    title = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    sort = db.Column(db.SmallInteger, index=True, default=1)
    type = db.Column(db.SmallInteger, index=True, default=1)
    isLock = db.Column(db.Boolean, index=True, default=True)
    interfaces = db.relationship('Interface', backref='menu')
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Menu %r>' % self.title


class Interface(db.Model):
    '''
    接口
    '''
    __tablename__ = 'db_interface'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    interface_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(36), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    isLock = db.Column(db.Boolean, index=True, default=True)
    menu_id = db.Column(db.String(36), db.ForeignKey('db_menu.menu_id'))
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Interface %r>' % self.name


class Document(db.Model):
    '''
    文档
    '''
    __tablename__ = 'db_document'
    id = db.Column(db.Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    document_id = db.Column(db.String(36), index=True, nullable=False, unique=True)
    user_id = db.Column(db.String(36), index=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    path = db.Column(db.String(255), nullable=False)
    type = db.Column(db.SmallInteger, index=True, default=1)
    ext = db.Column(db.String(64), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    __table_args__ = ({"useexisting": True})

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def __repr__(self):
        return '<Document %r>' % self.name