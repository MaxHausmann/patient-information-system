import sqlite3
import os
from sqlite3 import Error
from os.path import isfile

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.connection_handle = None
        self.connected = False

        if not isfile(filename):
            self.connect()
            self.setup()
            self.close_connection()
        else:
            self.connect()
        
    def connect(self):
        if not self.is_connected():
            try:
                self.connection_handle = sqlite3.connect(self.filename)
            except Error as e:
                print(e)
            self.connected = True

    def insert(self, table, fields, values):
        try:
            execute = self.execute("INSERT INTO " + str(table) + "(" + str(fields) + ") VALUES(" + Database.create_questionmarks(fields) + ")", values)
            return execute.lastrowid
        except Error as e:
            print(e)
            return False

    def update(self, table, fields, condition, values):
        try:
            return self.execute("UPDATE " + str(table) + " SET " + self.create_update_bindings(fields) + " " + condition, values)
        except Error as e:
            print(e)
            return False

    def _select(self, table, condition, values, what="*"):
        try:
            return self.execute("SELECT " + str(what) + " FROM " + str(table) + " " + condition, values)
        except Error as e:
            print(e)
            return False

    def select_all(self, table, condition, values):
        return self._select(table, condition, values)

    def exist(self, table, condition, values):
        fetch = self._select(table, condition, values, what="id").fetchone()
        if fetch != None:
            return True
        return False

    def execute(self, query, values=""):
        self.connect()
        cur = self.connection_handle.cursor()
        cur.execute(query, values)
        self.connection_handle.commit()
        return cur

    def setup(self):
        try:
            query = open("database/setup.sql", "r").read()
            cur = self.connection_handle.cursor()
            cur.executescript(query)
            self.connection_handle.commit()
            cur.close()
        except Error as e:
            self.connection_handle.rollback()
            os.remove(self.filename)
            print("Database setup failed: " + str(e))
            exit(1)

    def close_connection(self):
        self.connection_handle.close()
        self.connected = False

    def __del__(self):
        self.close_connection()

    def is_connected(self):
        return self.connected

    @staticmethod
    def create_questionmarks(fields):
        qm = ""
        for _ in range(0, fields.count(',')+1):
            qm += "?, "
        return qm[:-2]

    @staticmethod
    def create_update_bindings(fields):
        fields = str(fields).replace(",", "=?,")
        fields += "=?" # last field
        return fields

