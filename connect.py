# -*- coding: utf-8 -*-
# @Time    : 10/15/2020 5:43 PM
# @Author  : Enmo Ren
# @FileName: connect.py
# @Software: PyCharm

import json


import pymongo
import pymysql


class MongoClient(object):

    def __init__(self, addr=None, db=None, port=None, user=None, passwd=None):
        config = self.get_mongo_config(addr, db, port, user, passwd)
        client = pymongo.MongoClient(config['host'])
        self.client = client
        self.active_db = self.use_database(config.get('name'))

    def use_database(self, database_name):
        if not database_name:
            return None
        return self.client[database_name]

    def get_mongo_config(self, addr=None, db=None, port=None, user=None, passwd=None):
        if user and passwd:
            host = "mongodb://{}:{}@{}:{}/{}".format(user, passwd, addr, port, db)
        else:
            host = "mongodb://{}:{}".format(addr, port)
        return {
            'host': host,
            'maxPoolSize': 1000,
            'tz_aware': True,
            'socketTimeoutMS': None,
            'connectTimeoutMS': 1000,
            'w': 1,
            'wtimeout': 10000,
            'j': False,
            'name': db
        }

    def close(self):
        self.client.close()


class MySQLClient(object):

    def __init__(self, addr=None, db=None, user=None, pwd=None, port=3306):
        settings = self.get_mysql_config(addr, port, db, user, pwd)
        self.conn = pymysql.connect(**settings)

    @property
    def connect(self):
        return self.conn

    def get_mysql_config(self, addr=None, port=3306, db=None, user=None, passwd=None):
        return {
            "host": "{}".format(addr),
            "user": "{}".format(user),
            "passwd": "{}".format(passwd),
            "db": "{}".format(db),
            "charset": "utf8",
            'port': int(port),
            'autocommit': True
        }

    def execute_noquery_cmd(self, cmd: str, args=None, connect=None, callback=None):
        connect = connect or self.connect
        with connect.cursor() as cursor:
            r = cursor.execute(cmd, args)
            if not connect.autocommit_mode:
                connect.commit()
            if callback:
                callback(cmd, args, connect, cursor)
            return r

    def execute_noquery_many(self, cmd: str, *args, connect=None, callback=None):
        connect = connect or self.connect
        with connect.cursor() as cursor:
            r = cursor.executemany(cmd, list(args))
            if not connect.autocommit_mode:
                connect.commit()
            if callback:
                callback(cmd, args, connect, cursor)
            return r

    def query(self, cmd: str, args=None, connect=None, fetchall=False):
        result = []

        def query_callback(cmd, args, connect, cursor):
            if not fetchall:
                result.append(cursor.fetchone())
            else:
                result.extend(cursor.fetchall())

        self.execute_noquery_cmd(cmd, args, connect, query_callback)
        if not result:
            return None
        elif not fetchall:
            return result[0]
        else:
            return result

    def query_many(self, *cmdArgPairs, connect=None, fetchall=False) -> iter:
        connect = connect or self.connect
        with connect.cursor() as cursor:
            for cmd, args in cmdArgPairs:
                cursor.execute(cmd, args)
                if not connect.autocommit_mode:
                    connect.commit()
                if fetchall:
                    func = cursor.fetchall
                else:
                    func = cursor.fetchone
                yield func()

    def transaction(self, *cmdArgs, connect=None):
        connect = connect or self.connect
        cursor = connect.cursor()
        try:
            for cmd, args in cmdArgs:
                cursor.execute(cmd, args)
        except Exception as ex:
            connect.rollback()
        else:
            if not connect.autocommit_mode:
                connect.commit()
        finally:
            cursor.close()

    def close(self, conn=None):
        conn = conn or self.connect
        conn.close()
