# -*- coding: utf-8 -*-
# @Time    : 10/20/2020 1:27 PM
# @Author  : Enmo Ren
# @FileName: model.py
# @Software: PyCharm

from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators, FieldList, FormField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, DataRequired
from base import BaseForm as Form

class CrashReportForm(Form):
    data = StringField()