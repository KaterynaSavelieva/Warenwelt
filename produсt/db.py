import pymysql
from pymysql.cursors import DictCursor


def get_conn():
    """Create and return a connection to the onlineshop database."""
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="1111",
            database="onlineshop",
            cursorclass=DictCursor,
            autocommit=False
        )
        print("Connection successful!")   # ← message for a successful connection
        return conn
    except pymysql.MySQLError as err:
        print(f"Connection error: {err}")
        return None


if __name__ == "__main__":   # test — runs only when the file is executed directly
    conn = get_conn()
    if conn:
        conn.close()
