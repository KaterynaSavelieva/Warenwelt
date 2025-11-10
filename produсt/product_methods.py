from connection.storage import Storage
from pymysql import MySQLError
from tabulate import tabulate


class ProductMethods:
    # Methods for loading product data.

    def __init__(self):
        self.storage = Storage()
        self.storage.connect()


    def get_product(self, product_id: int):
        try:
            sql = "SELECT * FROM v_prod WHERE product_id = %s"
            row = self.storage.fetch_one(sql, params=(product_id,))
            if row:
                print(tabulate([row], headers="keys", tablefmt="rounded_grid"))
            else:
                print (f"No product found with ID {product_id}.")
            return row
        except MySQLError as e:
            print("Error loading product:", e)

    def get_all_products(self):
        try:
            sql = "SELECT * FROM v_prod ORDER BY product_id"
            results = self.storage.fetch_all(sql)
            if results:
                print(tabulate(results, headers="keys", tablefmt="rounded_grid"))
            else:
                print("No products found.")
            return results
        except MySQLError as e:
            print("Error loading all products:", e)
            return []


    def close(self):
        self.storage.disconnect()


# Test
if __name__ == "__main__":
    products = ProductMethods()
    products.get_all_products()
    products.get_product(12)
    products.get_product(1)
    products.close()
