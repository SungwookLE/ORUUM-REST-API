#  file: db_parser/dbModule.py
import os
import sys
sys.path.append(os.getcwd())
from backend.settings.base import BASE_DIR
import pymysql
import json

config_file = os.path.join(BASE_DIR, 'config.json') 
with open(config_file) as f:
    secrets = json.loads(f.read())

class Database():
    """
    raw SQL 문법으로 데이터베이스에 CRUD 수행하기 위해 해당 클래스 작성하였어요.
    그러나, 왠만해선 django ORM을 사용하여 database 핸들링해주세요.
    """

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user=secrets["db_config"]["user"],
                                  password=secrets["db_config"]["password"],
                                  db=secrets["db_config"]["schema"],
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        try:
            self.cursor.execute(query, args)

        except pymysql.err.IntegrityError as e:
            code, msg = e.args
            raise e

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()
