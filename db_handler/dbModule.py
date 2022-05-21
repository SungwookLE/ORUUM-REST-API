#  file: db_parser/dbModule.py
import os
import sys
sys.path.append(os.getcwd())

import pymysql
from config import db_config




class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password=db_config["password"],
                                  db='oruum_db',
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
