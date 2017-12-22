import pymysql
import traceback


class QueryClass(object):
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._db, self._cursor = self.connect()

    def connect(self):
        db = pymysql.connect(self.host, self.user,
                             self.password, self.database)
        cursor = db.cursor()
        return db, cursor

    def execute_query(self, _sql, _type):
        _db, _cursor = self._db, self._cursor
        if _db is None or _cursor is None:
            _db, _cursor = self.connect()

        try:
            _cursor.execute(_sql)
            if _type.upper() == 'SELECT':
                return self.get_data(_cursor)
            elif _type.upper().upper() == 'UPDATE':
                return self.update_data(_db)
            elif _type.upper().upper() == 'INSERT':
                return self.update_data(_db)
        except Exception as e:
            traceback.print_exc()
            print e.message
            return e.message
        _db.close()

    def close_connections(self):
        try:
            self._db.close()
            self._cursor.close()
        except Exception as e:
            print e.message

    @staticmethod
    def get_data(cursor):
        results = cursor.fetchall()
        return results

    @staticmethod
    def update_data(db):
        try:
            db.commit()
            return 1
        except:
            db.rollback()
            return 0
