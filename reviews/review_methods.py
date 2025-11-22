from connection.storage import Storage
import pymysql


class ReviewMethods:
    def __init__(self):
        self.storage = Storage()
        self.storage.connect()

    def get_all_reviews(self) -> list[dict]:
        """
        Load all reviews with customer name and product name.
        Visible for everyone.
        """
        sql = """
            SELECT
                r.review_id,
                r.rating,
                r.comment,
                r.review_date,
                c.name    AS customer_name,
                p.product AS product_name
            FROM review r
            JOIN customers c ON c.customer_id = r.customer_id
            JOIN product   p ON p.product_id   = r.product_id
            ORDER BY r.review_date DESC, r.review_id DESC
        """
        try:
            return self.storage.fetch_all(sql)
        except pymysql.MySQLError as e:
            print("Error loading reviews:", e)
            return []

    def get_purchased_products(self, customer_id: int) -> list[dict]:
        """
        Return DISTINCT products that this customer has bought.
        Can be used to build a dropdown list of products
        the customer is allowed to review.
        """
        sql = """
            SELECT DISTINCT
                p.product_id,
                p.product
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN product p      ON p.product_id = oi.product_id
            WHERE o.customer_id = %s
            ORDER BY p.product
        """
        try:
            return self.storage.fetch_all(sql, (customer_id,))
        except pymysql.MySQLError as e:
            print("Error loading purchased products:", e)
            return []

    def create_review(
        self,
        customer_id: int,
        product_id: int,
        rating: int,
        comment: str | None = None,
    ) -> bool:
        """
        Insert a new review.
        Allowed ONLY if customer has bought this product.
        """
        if rating < 1 or rating > 5:
            print("create_review: rating must be between 1 and 5")
            return False

        try:
            # 1) Check that customer really bought this product
            sql_check = """
                SELECT 1
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.order_id
                WHERE o.customer_id = %s
                  AND oi.product_id  = %s
                LIMIT 1
            """
            row = self.storage.fetch_one(sql_check, (customer_id, product_id))
            if not row:
                print("create_review: customer has not purchased this product.")
                return False

            # (optional) forbid a second review for the same product
            sql_exists = """
                SELECT 1
                FROM review
                WHERE customer_id = %s AND product_id = %s
                LIMIT 1
            """
            already = self.storage.fetch_one(sql_exists, (customer_id, product_id))
            if already:
                print("create_review: review for this product already exists.")
                return False

            # 2) Insert review
            sql_insert = """
                INSERT INTO review (customer_id, product_id, rating, comment)
                VALUES (%s, %s, %s, %s)
            """
            self.storage.execute(sql_insert, (customer_id, product_id, rating, comment))
            self.storage.connection.commit()
            return True

        except pymysql.MySQLError as e:
            print("Error creating review:", e)
            self.storage.connection.rollback()
            return False

    def close(self):
        self.storage.disconnect()
