# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from config import ChatConfig
from connect import MySQLClient

if __name__ == '__main__':
    create_time = int(time.time())
    client = MySQLClient(addr="mysql-virginia.cyqvleztnbng.us-east-1.rds.amazonaws.com", user="admin", port=3306, pwd="Santosvolpescope1",db="testdb1")
    add_sql = "insert into {} (token) values (%s);".format("S")
    client.execute_noquery_cmd(add_sql, args=("TESTTOKEN"))


