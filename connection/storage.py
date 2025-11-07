from connection.db import get_conn
from pymysql import MySQLError


class Storage:    #Storage class for database connection and queries.
    def __init__(self):
        # Attributes
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
    def execute(self, sql, params=None): # Execute INSERT, UPDATE, DELETE
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
            self.connection.commit()
        except MySQLError as e:
            print("Error executing query:", e)
            self.connection.rollback()

    def fetch_one(self, sql, params=None): # Execute SELECT and return one record
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    def fetch_all(self, sql, params=None): # Execute SELECT and return all records
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()


# test
if __name__ == "__main__":
    storage = Storage()
    storage.connect()

    rows = storage.fetch_all("SELECT * FROM product;")
    for row in rows:
        print(row)

    storage.disconnect()
