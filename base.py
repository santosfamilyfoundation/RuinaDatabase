# -*- coding: utf-8 -*-
# @Time    : 10/20/2020 1:30 PM
# @Author  : Enmo Ren
# @FileName: base.py
# @Software: PyCharm

from flask import request
from wtforms import Form
from libs.err_code import ParameterException


# TODO
class BaseForm(Form):
    def __init__(self):
        # data = request.json
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # error msg will be in form.errors
            raise ParameterException(msg=self.errors)
        return self  # send form back
