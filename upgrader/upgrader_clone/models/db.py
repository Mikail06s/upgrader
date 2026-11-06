import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class Database:
    """Singleton: одно соединение с БД на всё приложение."""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(**DB_CONFIG)
            except Error as e:
                print(f"[DB ERROR] Не удалось подключиться к MySQL: {e}")
                raise
        return self._connection

    def cursor(self, dictionary=True):
        return self.connect().cursor(dictionary=dictionary)

    def commit(self):
        self.connect().commit()

    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()


db = Database()
