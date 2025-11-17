from connection.db import get_conn
from pymysql import MySQLError

class Storage:    # Storage class for database connection and queries.
    def __init__(self):
        self.database_name = "onlineshop"
        self.connection = None

    # Connect
    def connect(self):
        try:
            self.connection = get_conn()
            if self.connection:
                print("Storage connected to database.")
            else:
                print("Database connection failed.")
        except MySQLError as e:
            print("Connection error:", e)

    # Disconnect
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    # Methods for Queries
    def execute(self, sql: str, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                self.connection.commit()
                if sql.lstrip().upper().startswith("INSERT"):
                    return cursor.lastrowid
                return cursor.rowcount
        except Exception as e:
            print("Error executing query:", e)
            self.connection.rollback()
            return None

    def fetch_one(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def fetch_all(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def insert_and_get_id(self, sql: str, params=None) -> int | None:
        try:
            with self.connection.cursor() as cur:
                cur.execute(sql, params)
                self.connection.commit() #!!!
                return cur.lastrowid or None
        except Exception as e:
            print("Error executing insert:", e)
            self.connection.rollback() #!!!
            return None


# test
if __name__ == "__main__":
    storage = Storage()
    storage.connect()

    rows = storage.fetch_all("SELECT * FROM product;")
    for row in rows:
        print(row)

    storage.disconnect()
