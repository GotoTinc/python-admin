#!/usr/bin/env python
# -*- coding:UTF-8 -*-
'''
@Description: 接口API
@Author: Zpp
@Date: 2019-10-14 13:50:25
@LastEditors  : Please set LastEditors
@LastEditTime : 2020-02-14 14:07:50
'''
from flask import Blueprint, request
from collection.interface import InterfaceModel
from ..token_auth import auth, validate_current_access
from libs.code import ResultDeal

route_interface = Blueprint('Interface', __name__, url_prefix='/v1/Interface')


@route_interface.route('/CreateInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def CreateInterface():
    params = {
        'name': request.form.get('name'),
        'path': request.form.get('path'),
        'method': request.form.get('method'),
        'description': request.form.get('description'),
        'menu_id': request.form.get('menu_id'),
        'mark': request.form.get('mark')
    }

    result = InterfaceModel().CreateInterfaceRequest(params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/LockInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def LockInterface():
    result = InterfaceModel().LockInterfaceRequest(
        interface_id=request.form.getlist('interface_id[]'), 
        is_disabled=True if request.form.get('is_disabled') == 'true' else False
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
    return ResultDeal(data=result)


@route_interface.route('/DelInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def DelInterface():
    result = InterfaceModel().DelInterfaceRequest(interface_id=request.form.getlist('interface_id[]'))
    
    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)
        
    return ResultDeal(data=result)


@route_interface.route('/ModifyInterface', methods=['POST'])
@auth.login_required
@validate_current_access
def ModifyInterface():
    params = {
        'name': request.form.get('name'),
        'path': request.form.get('path'),
        'method': request.form.get('method'),
        'description': request.form.get('description'),
        'menu_id': request.form.get('menu_id'),
        'mark': request.form.get('mark')
    }

    result = InterfaceModel().ModifyInterfaceRequest(interface_id=request.form.get('interface_id'), params=params)

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)


@route_interface.route('/QueryInterfaceByParam', methods=['POST'])
@auth.login_required
@validate_current_access
def QueryInterfaceByParam():
    params = {}
    if request.form.get('is_disabled'):
        params['is_disabled'] = True if request.form.get('is_disabled') == 'true' else False
    Ary = ['name', 'method']
    for i in Ary:
        if request.form.get(i):
            params[i] = request.form.get(i)

    result = InterfaceModel().QueryInterfaceByParamRequest(
        params=params,
        page=int(request.form.get('page')),
        page_size=int(request.form.get('page_size')),
        order_by=request.form.get('order_by', None)
    )

    if type(result).__name__ == 'str':
        return ResultDeal(msg=result, code=-1)

    return ResultDeal(data=result)
