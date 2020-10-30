# -*- coding: utf-8 -*-
# @Time    : 10/20/2020 1:24 PM
# @Author  : Enmo Ren
# @FileName: run.py
# @Software: PyCharm

from flask import Flask, request, g, jsonify
from gevent import pywsgi
import json
from scheduler import Scheduler
from model import CrashReportForm
from config import ChatConfig



app = Flask(__name__)
app.config.from_object(ChatConfig)


@app.route('/v1', methods=['POST'])
def index():
    return 'HomePage'


@app.route('/v1/addReport', methods=['POST'])
def report_deal():
    report_form = request.get_json(silent=True)
    # report_form = CrashReportForm().validate_for_api()
    data = json.dumps(report_form)
    s = Scheduler()
    res = s.save_database(data)
    if res == 1:
        return jsonify({"code": 200, "msg": "success"})
    # TODO define error code

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5006), app)
    server.serve_forever()