import sqlite3


class DbHandler:
    def __init__(self, dbname):
        self._dbname = dbname
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._dbname)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._cursor.close()
            self._conn.close()
        except AttributeError:
            print('Not closable')
            return True

    def execute(self, sql):
        print(sql)
        try:
            self._cursor.execute(sql)
        except sqlite3.OperationalError:
            print('skip sqlite error')

    def fetchone(self, sql):
        print(sql)
        try:
            self._cursor.execute(sql)
            return self._cursor.fetchone()
        except sqlite3.OperationalError:
            print('fetchone: skip error & return None')
            return None

    def fetchall(self, sql):
        print(sql)
        try:
            self._cursor.execute(sql)
            return self._cursor.fetchall()
        except sqlite3.OperationalError:
            print('fetchall: skip error and return None')
            return None

    def commit(self):
        self._conn.commit()

    def run(self, sql):
        self.execute(sql)
        self.commit()
