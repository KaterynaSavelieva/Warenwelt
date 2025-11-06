from typing import List, Dict, Any, Optional
from db import get_conn
from tabulate import tabulate

class Storage: # Handles database connection and product queries.

    def __init__(self):#Initialize the connection and cursor.
        self.db_connection = get_conn()
        self.cursor = self.db_connection.cursor()

    # ---------- helpers ----------
    def _commit(self): #"_" - protected, means “internal helper, don’t use outside Storage”.
        self.db_connection.commit()
    def _rollback(self):
        self.db_connection.rollback()

    # ---------- READ ----------
    def get_product(self, product_id):
        query = """
            SELECT * 
            FROM v_tab 
            WHERE id = %s
        """
        self.cursor.execute(query, (product_id,)) # The comma creates a one-item tuple; without it, product_id would not be a tuple
        return self.cursor.fetchone()  # Returns a single row as a dictionary or None
    def print_one_product(self, product_id): #Print one product in a formatted table.
        product = self.get_product(product_id)
        if not product:
            print("No product found.")
        else:
            print(tabulate([product], headers="keys", tablefmt='plain'))

    def list_products(self):# Select all products from the database view v_tab.
        query = """
            SELECT *
            FROM v_tab
            ORDER BY id DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Returns all rows as a list of dictionaries
    def print_products(self): #Print all products in a formatted table.
        products = self.list_products()
        if not products:
            print("No products found.")
        else:
            print(tabulate(products, headers="keys", tablefmt="rounded_grid"))
            #print(tabulate(products, headers=['ID', 'Name'], tablefmt='rounded_grid'))
            # or, if you want a custom subset/order, map them explicitly and ensure key names match:
            #cols = ["id", "name", "kategorie", "preis", "gewicht"]
            #print(tabulate([{k: p.get(k) for k in cols} for p in products], headers=cols, tablefmt="rounded_grid"))

    # ---------- CREATE ----------
    def create_product(self, product_obj):
        row = product_obj.to_row
        cat =row["category"]

        try:
            # 1) base table
            self.cursor.execute(
                """
                INSERT INTO product (name, price, category) 
                VALUES (%s, %s, %s)
                """,
                (row["name"], row["price"], cat),
            )
            new_id = self.cursor.lastrowid

            # 2) category-specific table
            if cat == "electronics":
                self.cursor.execute(
                    """
                    INSERT INTO electronics (id, brand, warranty_years)
                    VALUES (%s, %s, %s),
                    """,
                    (new_id, row["brand"], row["warranty_years"]),
                )
            elif cat == "clothing":
                self.cursor.execute(
                    """
                    INSERT INTO clothing (id, size)
                    VALUES (%s, %s)
                    """,
                    (new_id, row["size"]),
                )
            elif cat == "books":
                self.cursor.execute(
                    """
                    INSERT INTO books (id, author, page_count)
                    VALUES (%s, %s, %s)
                    """,
                    (new_id, row["author"], row["page_count"]),
                )
            else:
                raise ValueError(f"Unknown category: {cat}")
            self._commit()
            return new_id
        except Exception:
            self._rollback()
            raise



    # ---------- UPDATE ----------
    def update_product(self, product_obj):
        row = product_obj.to_row()
        if not row.get(""):
            raise ValueError ("update_product: product id is required")
        cat = row["category"]

        try:
            # 1) base table
            self.cursor.execute(
                """
                UPDATE product 
                SET name = %s, price = %s, weight = %s
                WHERE id = %s
                """,
                (row["name"], row["price"], row["weight"], row["id"]),
            )
            # 2) category-specific table
            if cat =="electronics":
                self.cursor.execute(
                    """
                    UPDATE electronics
                    SET brand %s, warranty_years %s
                    WHERE id = %s
                    """,
                    (row["brand"], row["warranty_years"], row["id"]),
                )
            elif cat =="clothing":
                self.cursor.execute(
                    """
                    UPDATE clothing
                    SET size = %s
                    WHERE id = %s
                    """,
                    (row["size"], row["id"]),
                )
            elif cat =="books":
                self.cursor.execute(
                    """
                    UPDATE books
                    SET author = %s, page_count = %s
                    WHERE id = %s
                    """,
                    (row ["autor"], row["page_count"])
                )
            else:
                raise ValueError(f"Unknown category: {cat}")
            self._commit()
        except Exception:
            self._rollback()
            raise

    # ---------- DELETE ----------
    def delete_product(self, product_id):
        try:
            self.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
            self._commit()
        except Exception:
            self._rollback()
            raise


    # ---------- cleanup ----------
    def close(self): #Close the database connection.
        self.cursor.close()
        self.db_connection.close()

if __name__ == "__main__":
    storage = Storage()
    storage.print_products()
    storage.close()
