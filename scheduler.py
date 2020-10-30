# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from config import ChatConfig
from connect import MySQLClient

class Scheduler(object):

    def __init__(self):
        self.client = MySQLClient(**ChatConfig.MYSQL_CONFIG)

    def save_database(self, data):
        add_sql = "insert into {} (data) values (%s);".format("js_data")
        res = self.client.execute_noquery_cmd(add_sql, args=data)
        return res

