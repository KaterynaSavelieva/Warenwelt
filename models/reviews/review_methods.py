from idlelib.multicall import r

from connection.storage import Storage
import pymysql
from tabulate import tabulate

class ReviewMethods:
    """
    Methods for working with reviews from console and web.
    Uses Storage for DB access and prints human-readable output
    for console usage.
    """

    def __init__(self):
        self.storage = Storage()
        self.storage.connect()

    @staticmethod
    def _print_line():
        print("-" * 60)

    def get_all_reviews(self) -> list[dict]:
        """
        Load all reviews with customer name and product name.
        Visible for everyone (used mainly for debugging).
        """
        sql = """
            SELECT
                r.review_id,
                r.rating,
                r.comment,
                r.created_at,
                c.name    AS customer_name,
                p.product AS product_name
            FROM review r
            JOIN customers c ON c.customer_id = r.customer_id
            JOIN product   p ON p.product_id   = r.product_id
            ORDER BY r.created_at DESC, r.review_id DESC
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
        rating: float,
        comment: str | None = None,
    ) -> bool:
        """
        Insert a new review.
        Allowed ONLY if customer has bought this product.
        """
        # simple validation of rating
        if rating < 1 or rating > 5:
            print("create_review: rating must be between 1 and 5.")
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
            print("Review created successfully.")
            return True

        except pymysql.MySQLError as e:
            print("Error creating review:", e)
            self.storage.connection.rollback()
            return False

    def get_reviews_for_product(self, product_id: int) -> list[dict]:
        sql = """SELECT 
                    product_total_reviews,
                    product_name,
                    product_average_rating,
                    review_date,
                    review_rating,
                    review_comment
                FROM v_rating WHERE product_id = %s"""
        try:
            rows = self.storage.fetch_all(sql, (product_id,))
        except pymysql.MySQLError as e:
            print("Error loading reviews for product:", e)
            return []
        if not rows:
            print(f"No reviews found for product ID {product_id}.")
            return []

        total_reviews = rows[0]["product_total_reviews"]
        product_name = rows[0]["product_name"]
        avg_rating = rows[0]["product_average_rating"]
        print(f"Total {total_reviews} reviews for product ID {product_id} {product_name}, average rating: {avg_rating}/5")

        table_rows = [
            {
                "review_date": r["review_date"],
                "rating": r["review_rating"],
                "comment": r["review_comment"],
            }
            for r in rows
        ]
        print(tabulate(table_rows, headers="keys", tablefmt="rounded_grid"))

        return rows

    def get_rating_summary_for_product(self, product_id: int) -> dict | None:
        sql = """
            SELECT
                p.product_id,
                p.product       AS product_name,
                COUNT(r.review_id) AS review_count,
                AVG(r.rating)      AS avg_rating,
                MIN(r.rating)      AS min_rating,
                MAX(r.rating)      AS max_rating
            FROM product p
            LEFT JOIN review r ON r.product_id = p.product_id
            WHERE p.product_id = %s
            GROUP BY p.product_id, p.product
        """
        try:
            row = self.storage.fetch_one(sql, (product_id,))
        except pymysql.MySQLError as e:
            print("Error loading rating summary for product:", e)
            return None

        if not row:
            print(f"Product with ID {product_id} not found.")
            return None

        print(f"Rating summary for product [{row['product_id']}] {row['product_name']}:")
        if row["review_count"] == 0:
            print("No reviews yet.")
        else:
            print(f"Reviews: {row['review_count']}")
            print(f"Average rating: {float(row['avg_rating']):.2f}/5")
            print(f"Min rating: {float(row['min_rating']):.1f}")
            print(f"Max rating: {float(row['max_rating']):.1f}")

        return row

    def get_reviews_for_customer(self, customer_id: int) -> list[dict]:
        sql = """
            SELECT
                r.review_id,
                r.rating,
                r.comment,
                r.created_at,
                c.name    AS customer_name,
                p.product AS product_name
            FROM review r
            JOIN customers c ON c.customer_id = r.customer_id
            JOIN product   p ON p.product_id   = r.product_id
            WHERE c.customer_id = %s
            ORDER BY r.created_at DESC, r.review_id DESC
        """
        try:
            rows = self.storage.fetch_all(sql, (customer_id,))
            print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
        except pymysql.MySQLError as e:
            print("Error loading reviews for customer:", e)
            return []

        if not rows:
            print(f"No reviews found for customer ID {customer_id}.")
            return []

        customer_name = rows[0]["customer_name"]
        self._print_line()
        print(f"Reviews written by customer [{customer_id}] {customer_name}:")
        self._print_line()

        for r in rows:
            comment = r["comment"] or "-"
            date = r.get("review_date") or ""
            print(
                f"[{r['review_id']}] "
                f"{date} | {r['rating']}/5 "
                f"for {r['product_name']}: {comment}"
            )

        self._print_line()
        print(f"Total: {len(rows)} review(s).")
        return rows

    def get_rating_summary_for_customer(self, customer_id: int) -> dict | None:
        sql = """
            SELECT
                c.customer_id,
                c.name AS customer_name,
                COUNT(r.review_id) AS review_count,
                AVG(r.rating)      AS avg_rating,
                MIN(r.rating)      AS min_rating,
                MAX(r.rating)      AS max_rating
            FROM customers c
            LEFT JOIN review r ON r.customer_id = c.customer_id
            WHERE c.customer_id = %s
            GROUP BY c.customer_id, c.name
        """
        try:
            row = self.storage.fetch_one(sql, (customer_id,))
        except pymysql.MySQLError as e:
            print("Error loading rating summary for customer:", e)
            return None

        if not row:
            print(f"Customer with ID {customer_id} not found.")
            return None

        self._print_line()
        print(f"Rating summary for customer [{row['customer_id']}] {row['customer_name']}:")
        if row["review_count"] == 0:
            print("No reviews written yet.")
        else:
            print(f"Reviews: {row['review_count']}")
            print(f"Average rating: {float(row['avg_rating']):.2f}/5")
            print(f"Min rating: {float(row['min_rating']):.1f}")
            print(f"Max rating: {float(row['max_rating']):.1f}")
        self._print_line()

        return row

    def delete_review(self, review_id: int) -> bool:
        try:
            # 1) Load review info
            sql_select = """
                SELECT
                    r.review_id,
                    r.rating,
                    r.comment,
                    r.created_at,
                    c.name    AS customer_name,
                    p.product AS product_name
                FROM review r
                JOIN customers c ON c.customer_id = r.customer_id
                JOIN product   p ON p.product_id   = r.product_id
                WHERE r.review_id = %s
            """
            row = self.storage.fetch_one(sql_select, (review_id,))
            if not row:
                print(f"Review with ID {review_id} not found.")
                return False

            # 2) Delete review
            sql_delete = "DELETE FROM review WHERE review_id = %s"
            self.storage.execute(sql_delete, (review_id,))
            self.storage.connection.commit()

            print(
                f"Review [{review_id}] for product '{row['product_name']}' "
                f"by {row['customer_name']} deleted."
            )
            return True

        except pymysql.MySQLError as e:
            print("Error deleting review:", e)
            self.storage.connection.rollback()
            return False

    def close(self):
        self.storage.disconnect()