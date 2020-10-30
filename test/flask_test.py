# -*- coding: utf-8 -*-
# @Time    : 10/31/2020 12:20 AM
# @Author  : Enmo Ren
# @FileName: flask_test.py
# @Software: PyCharm

import os
import unittest

from run import app

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        # mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_add_report(self):
        response = self.app.post('/v1/addReport', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()