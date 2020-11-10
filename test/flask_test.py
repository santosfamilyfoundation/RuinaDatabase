# -*- coding: utf-8 -*-
# @Time    : 10/31/2020 12:20 AM
# @Author  : Enmo Ren
# @FileName: flask_test.py
# @Software: PyCharm

import os
import unittest
from config import ChatConfig
from connect import MySQLClient
from run import app
import json

TEST_DB = 'test.db'


class TestDB(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()
        url = ChatConfig.MYSQL_CONFIG
        if not url:
            self.skipTest("No database URL set")
        self.client = MySQLClient(**url)
        if self.client.conn:
            self.client.execute_noquery_cmd("CREATE DATABASE testdb111")

    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_add_report(self):
        payload = json.dumps({
            "data": "DB Testing",
        })
        response = self.app.post('/v1/addReport', headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()