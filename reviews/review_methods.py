from connection.storage import Storage
from datetime import date
from tabulate import tabulate
class ReviewMethods:

    def __init__(self):
        # Create a connection to the database
        self.storage = Storage()
        self.storage.connect()

    def save_review(self, customer_id: int, product_id: int, rating: float, comment: str = ""):
        #Save a new review into the database.

        # Check rating range
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return None

        sql = """
        INSERT INTO review (customer_id, product_id, rating, comment, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (customer_id, product_id, rating, comment, date.today())

        try:
            # Insert and get new review ID
            review_id = self.storage.insert_and_get_id(sql, params)
            print(f"Review saved with ID {review_id}")
            return review_id
        except Exception as e:
            print("Error while saving review:", e)
            return None


    def get_reviews_for_product(self, product_id: int) -> list[dict]:
        sql = """
        SELECT review_id, customer_id, product_id, rating, comment, created_at
        FROM review
        WHERE product_id = %s
        ORDER BY created_at DESC
        """
        try:
            rows = self.storage.fetch_all(sql, (product_id,))
            if rows:
                print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
            else:
                print(f"No reviews found for product ID {product_id}.")
            return rows
        except Exception as e:
            print("Error while reading product reviews:", e)
            return []

    def get_rating_summary_for_product(self, product_id: int) -> dict:
        sql = "SELECT * FROM v_rating_summary_for_product WHERE product_id = %s"
        try:
            row = self.storage.fetch_one(sql, params=(product_id,))
            if row:
                print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
            else:
                print(f"No rating summary found for product ID {product_id}.")
            return row or {}
        except Exception as e:
            print("Error reading product rating summary:", e)
            return {}

    def get_reviews_for_customer(self, customer_id: int) -> list[dict]:
        sql = """
        SELECT review_id, customer_id, product_id, rating, comment, created_at
        FROM review
        WHERE customer_id = %s
        ORDER BY created_at DESC
        """
        try:
            rows = self.storage.fetch_all(sql, (customer_id,))
            if rows:
                print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
            else:
                print(f"No reviews found for customer ID {customer_id}.")
            return rows
        except Exception as e:
            print("Error while reading customer reviews:", e)
            return []

    def get_rating_summary_for_customer(self, customer_id: int) -> dict:
        sql = "SELECT * FROM v_rating_summary_for_customer WHERE customer_id = %s"
        try:
            row = self.storage.fetch_one(sql, params=(customer_id,))
            if row:
                print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
            else:
                print(f"No rating summary found for customer ID {customer_id}.")
            return row or {}
        except Exception as e:
            print("Error reading customer rating summary:", e)
            return {}

    def delete_review(self, review_id: int):    #Delete one review by its ID
        sql = "DELETE FROM review WHERE review_id = %s"
        try:
            self.storage.execute(sql, (review_id,))
            print(f"Review {review_id} deleted.")
            return True
        except Exception as e:
            print(" Error while deleting review:", e)
            return False


    def close(self):
        self.storage.disconnect()
