# -*- coding: utf-8 -*-
# @Time    : 10/20/2020 1:30 PM
# @Author  : Enmo Ren
# @FileName: base.py
# @Software: PyCharm

from flask import request
from wtforms import Form
from libs.err_code import ParameterException


# TODO 获取数据 抛出异常
class BaseForm(Form):
    def __init__(self):
        # data = request.json
        # 静默模式，意思说不要报错
        data = request.get_json(silent=True)
        args = request.args.to_dict()  # get请求参数的时候，配合下面**args将get请求参数传过去
        super(BaseForm, self).__init__(data=data, **args)

    # 实现了在发生错误的时候会打印json格式的错误信息
    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # 所有的错误信息都在Form.errors中
            raise ParameterException(msg=self.errors)
        return self  # 把form返回回去
