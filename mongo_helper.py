# -*- coding: utf-8 -*-
# @Time    : 10/10/2020 2:32 AM
# @Author  : Enmo Ren
# @FileName: mongo_helper.py
# @Software: PyCharm

import pymongo


class MG(object):
    def __init__(self, address=None, db=None, port=None, user=None, pwd=None):
        config = self.get_mongodb_config(address, db, port, user, pwd)
        self.client = pymongo.MongoClient(config['host'])
        self.db = self.use_database(config.get('name'))

    def use_database(self, database_name):
        if not database_name:
            return None
        return self.client[database_name]

    @staticmethod
    def get_mongodb_config(address=None, db=None, port=None, user=None, pwd=None):
        if user and pwd:
            host = "mongodb://{}:{}@{}:{}/{}".format(user, pwd, address, port, db)
        else:
            host = "mongodb://{}:{}".format(address, port)
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


"""
mongodb_operation 静态方法 用来和mongodb 操作交互 
"""


class BaseHandle(object):
    @staticmethod
    def insert_one(collection, data: dict):
        """直接使用insert() 可以插入一条和插入多条 不推荐 明确区分比较好"""
        res = collection.insert_one(data)
        return res.inserted_id

    @staticmethod
    def insert_many(collection, data_list):
        res = collection.insert_many(data_list)
        return res.inserted_ids

    @staticmethod
    def find_one(collection, data, data_field: dict):
        if len(data_field):
            res = collection.find_one(data, data_field)
        else:
            res = collection.find_one(data)
        return res

    @staticmethod
    def find_many(collection, data, data_field: dict):
        """ data_field 是指输出 操作者需要的字段"""
        if len(data_field):
            res = collection.find(data, data_field)
        else:
            res = collection.find(data)
        return res

    @staticmethod
    def update_one(collection, data_condition, data_set):
        """修改一条数据"""
        res = collection.update_one(data_condition, data_set)
        return res

    @staticmethod
    def update_many(collection, data_condition, data_set):
        """ 修改多条数据 """
        res = collection.update_many(data_condition, data_set)
        return res

    @staticmethod
    def replace_one(collection, data_condition, data_set):
        """ 完全替换掉 这一条数据， 只是 _id 不变"""
        res = collection.replace_one(data_condition, data_set)
        return res

    @staticmethod
    def delete_many(collection, data):
        res = collection.delete_many(data)
        return res

    @staticmethod
    def delete_one(collection, data):
        res = collection.delete_one(data)
        return res


'''
mongodb_base 和mongo 连接的信息 
'''


class DBBase(object):
    """ 各种query 中的数据 data 和 mongodb 文档中的一样"""

    def __init__(self, address, db, port, collection, user=None, pwd=None):
        self.mg = MG(address, db, port, user, pwd)
        self.collection = self.mg.db[collection]

    def insert_one(self, data):
        res = BaseHandle.insert_one(self.collection, data)
        return res

    def insert_many(self, data_list):
        res = BaseHandle.insert_many(self.collection, data_list)
        return res

    def find_one(self, data, data_field: dict):
        res = BaseHandle.find_one(self.collection, data, data_field)
        return res

    def find_many(self, data, data_field: dict):
        """ 有多个键值的话就是 AND 的关系"""
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_all(self, data: dict, data_field: dict):
        """select * from table"""
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_in(self, field, item_list, data_field: dict):
        """SELECT * FROM inventory WHERE status in ("A", "D")"""
        data = dict()
        data[field] = {"$in": item_list}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_or(self, data_list, data_field: dict):
        """db.inventory.find(
                {"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]}
            )

        SELECT * FROM inventory WHERE status = "A" OR qty < 30
        """
        data = dict()
        data["$or"] = data_list
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_between(self, field, value1, value2, data_field: dict):
        """获取俩个值中间的数据"""
        data = dict()
        data[field] = {"$gt": value1, "$lt": value2}
        # data[field] = {"$gte": value1, "$lte": value2} # <>   <= >=
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_more(self, field, value, data_field: dict):
        data = dict()
        data[field] = {"$gt": value}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_less(self, field, value, data_field: dict):
        data = dict()
        data[field] = {"$lt": value}
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def find_like(self, field, value, data_field: dict):
        """ where key like "%audio% """
        data = dict()
        data[field] = {'$regex': '.*' + value + '.*'}
        print(data)
        res = BaseHandle.find_many(self.collection, data, data_field)
        return res

    def delete_one(self, data):
        """ 删除单行数据 如果有多个 则删除第一个"""
        res = BaseHandle.delete_one(self.collection, data)
        return res

    def delete_many(self, data):
        """ 删除查到的多个数据 data 是一个字典 """
        res = BaseHandle.delete_many(self.collection, data)
        return res


if __name__ == '__main__':
    mongodb_config = {
        "address": '52.82.59.2',
        "port": 27017,
        "db": "admin",
        "collection": "logs"
    }
    mongodb_conn = DBBase(**mongodb_config)

    log_data = [
        {"timestamp": 1596704219, "user_id": "xxx", "context": "xxx"},
        {"timestamp": 7878787887, "user_id": "xxx", "context": "xxx"},
    ]

    mongodb_conn.insert_many(log_data)
