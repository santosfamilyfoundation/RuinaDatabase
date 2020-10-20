# -*- coding: utf-8 -*-
# @Time    : 10/20/2020 1:24 PM
# @Author  : Enmo Ren
# @FileName: run.py
# @Software: PyCharm

from flask import Flask, request, g, jsonify
from gevent import pywsgi
from model import CrashReportForm



app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/v1', methods=['POST'])
def index():
    return 'HomePage'


@app.route('/v1/addReport', methods=['POST'])
def report_deal():
    report_form = CrashReportForm().validate_for_api()
    data = report_form.data.data
    print(data)
    return jsonify({"code": 200, "msg": "success"})

if __name__ == '__main__':

    server = pywsgi.WSGIServer(('0.0.0.0', 5006), app)
    server.serve_forever()