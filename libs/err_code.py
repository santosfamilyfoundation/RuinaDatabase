# -*- coding: utf-8 -*-
# @Time    : 10/20/2020 1:31 PM
# @Author  : Enmo Ren
# @FileName: err_code.py
# @Software: PyCharm

from libs.error import APIException


class ParameterException(APIException):
    '''
    为所有的校验失败定义的错误类
    '''
    code = 400
    msg = 'invalid parameter'
    error_code = 400