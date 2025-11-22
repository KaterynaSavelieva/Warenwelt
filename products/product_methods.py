from connection.storage import Storage
from pymysql import MySQLError
from tabulate import tabulate

class ProductMethods:
    def __init__(self):
        self.storage = Storage()
        self.storage.connect()

        # IMPORTANT: always see latest committed data
        try:
            self.storage.connection.autocommit(True)
        except Exception as e:
            print("Could not enable autocommit for ProductMethods:", e)

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

    def get_all_products1(self):
        try:
            sql = """
                SELECT
                    p.product_id,
                    p.product,
                    p.category,
                    p.price,
                    p.brand,
                    p.warranty_years,
                    p.size,
                    p.author,
                    p.page_count,
                    ar.avg_rating,
                    ar.review_count
                FROM v_prod p
                LEFT JOIN (
                    SELECT
                        product_id,
                        AVG(rating) AS avg_rating,
                        COUNT(*)    AS review_count
                    FROM review
                    GROUP BY product_id
                ) ar ON ar.product_id = p.product_id
                ORDER BY p.product_id
            """
            #sql = "SELECT * FROM v_prod ORDER BY product_id"
            results = self.storage.fetch_all(sql)
            if results:
                print(tabulate(results, headers="keys", tablefmt="rounded_grid"))
            else:
                print("No products found.")
            return results
        except MySQLError as e:
            print("Error loading all products:", e)
            return []

    def get_all_products2(self) -> list[dict]:
        """
        Load all products with category-specific fields and aggregated rating.
        """
        sql = """
            SELECT
                product_id,
                product,
                price,
                weight,
                category,
                brand,
                warranty_years,
                size,
                author,
                page_count,
                avg_rating,
                review_count
            FROM v_prod
            ORDER BY product_id
        """
        try:
            rows = self.storage.fetch_all(sql)
            # Якщо потрібно красиве виведення в консолі:
            # if rows:
            #     print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
            return rows
        except Exception as e:
            print("Error loading all products:", e)
            return []

    def get_all_products(self) -> list[dict]:
        """
        Load all products with category-specific fields and aggregated rating.
        """
        sql = """
            SELECT
                product_id,
                product,
                price,
                weight,
                category,
                brand,
                warranty_years,
                size,
                author,
                page_count,
                avg_rating,
                review_count
            FROM v_prod
            ORDER BY product_id
        """
        try:
            rows = self.storage.fetch_all(sql)
            return rows
        except Exception as e:
            print("Error loading all products:", e)
            return []

    def save_product(self, *, product_new: str, price: float, weight: float, category: str,  author: str | None = None, page_count: int | None = None, brand: str | None = None, warranty_years: int | None = None, size: str | None = None) -> int | None:
        try:
            # 1️ Мінімальна перевірка
            product_new = (product_new or "").strip()
            if not product_new:
                print("Product name required.");
                return None
            if price is None or float(price) <= 0:
                print("Price must be > 0.");
                return None
            if weight is None or float(weight) < 0:
                print("Weight must be >= 0.");
                return None
            if category not in ("electronics", "clothing", "books"):
                print("Category must be 'electronics', 'clothing' or 'books'.");
                return None

            # 2 Обов’язкові поля підкатегорій
            if category == "books" and (not author or page_count is None):
                print("Books need 'author' and 'page_count'.");
                return None
            if category == "electronics" and (not brand or warranty_years is None):
                print("Electronics need 'brand' and 'warranty_years'.");
                return None
            if category == "clothing" and not size:
                print("Clothing needs 'size'.");
                return None

            # 3️ Перевірка на дубль (product + category)
            dup = self.storage.fetch_one(
                "SELECT product_id FROM product WHERE product=%s AND category=%s",
                (product_new, category)
            )
            if dup:
                print(f"Product already exists (ID {dup['product_id']}). No insert.")
                return dup["product_id"]

            # 4️ Транзакція
            self.storage.connection.begin()

            sql_p = """
                INSERT INTO product (product, price, weight, category)
                VALUES (%s, %s, %s, %s)
            """
            new_id = self.storage.insert_and_get_id(sql_p, (product_new, price, weight, category))
            if not new_id:
                raise RuntimeError("Insert failed: no new ID returned.")

            # 5 Вставка у підтаблицю
            if category == "books":
                self.storage.execute(
                    "INSERT INTO books (product_id, author, page_count) VALUES (%s, %s, %s)",
                    (new_id, author, page_count)
                )
            elif category == "electronics":
                self.storage.execute(
                    "INSERT INTO electronics (product_id, brand, warranty_years) VALUES (%s, %s, %s)",
                    (new_id, brand, warranty_years)
                )
            else:  # clothing
                self.storage.execute(
                    "INSERT INTO clothing (product_id, size) VALUES (%s, %s)",
                    (new_id, size)
                )

            self.storage.connection.commit()
            print(f"Product saved with ID {new_id}.")
            return new_id

        except Exception as e:
            self.storage.connection.rollback()
            print("Error saving product:", e)
            return None

    def update_product(self, product_id: int, *, name: str | None = None, price: float | None = None, weight: float | None = None) -> bool:
        """Просте оновлення базових даних продукту."""
        try:
            # Формуємо динамічний SQL тільки для наявних полів
            updates = []
            values = []
            if name:
                updates.append("product = %s")
                values.append(name)
            if price is not None:
                updates.append("price = %s")
                values.append(price)
            if weight is not None:
                updates.append("weight = %s")
                values.append(weight)

            if not updates:
                print("Nothing to update.")
                return False

            sql = f"UPDATE product SET {', '.join(updates)} WHERE product_id = %s"
            values.append(product_id)

            affected = self.storage.execute(sql, tuple(values))
            if affected:
                self.storage.connection.commit()
                print(f"Product ID {product_id} updated successfully.")
                return True
            else:
                print("No product updated.")
                return False

        except MySQLError as e:
            self.storage.connection.rollback()
            print("Database error during update:", e)
            return False
        except Exception as e:
            print("Unexpected error:", e)
            return False

    def delete_product(self, product_id: int) -> bool:
        """Видаляє продукт за ID (разом із підтаблицею завдяки CASCADE)."""
        try:
            sql = "DELETE FROM product WHERE product_id = %s"
            affected = self.storage.execute(sql, (product_id,))
            if affected:
                self.storage.connection.commit()
                print(f"Product ID {product_id} deleted successfully.")
                return True
            else:
                print(f"No product found with ID {product_id}.")
                return False
        except MySQLError as e:
            self.storage.connection.rollback()
            print("Database error during delete:", e)
            return False
        except Exception as e:
            print("Unexpected error:", e)
            return False

    def find_products_by_category(self, category: str) -> list[dict]:
        if category not in ("electronics", "clothing", "books"):
            print("Category must be 'electronics' | 'clothing' | 'books'.");
            return []
        rows = self.storage.fetch_all(
            "SELECT * FROM v_prod WHERE category=%s ORDER BY product_id", (category,)
        )
        if rows:
            print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
        else:
            print("No products for this category.")
        return rows or []

    def find_products_under_price(self, max_price: float) -> list[dict]:
        rows = self.storage.fetch_all(
            "SELECT * FROM v_prod WHERE price <= %s ORDER BY price, product_id", (max_price,)
        )
        if rows:
            print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
        else:
            print("No products under this price.")
        return rows or []

    def get_products_filtered1(
        self,
        *,
        search: str = "",
        category: str = "",
        brand: str = "",
        author: str = "",
        size: str = "",
        sort: str = "id",        # можна ігнорувати, сортуємо у Python
        direction: str = "asc",  # те саме
    ) -> list[dict]:
        """
        Load products with optional filters and rating info.

        Returns rows with:
        product_id, product, category, price,
        brand, warranty_years, size, author, page_count,
        avg_rating, review_count
        """

        sql = """
            SELECT
                p.product_id,
                p.product,
                p.category,
                p.price,

                e.brand,
                e.warranty_years,

                cl.size,
                b.author,
                b.page_count,

                r.avg_rating,
                r.review_count
            FROM product p
            LEFT JOIN electronics e
                ON e.product_id = p.product_id
            LEFT JOIN clothing cl
                ON cl.product_id = p.product_id
            LEFT JOIN books b
                ON b.product_id = p.product_id
            LEFT JOIN (
                SELECT
                    product_id,
                    ROUND(AVG(rating), 1) AS avg_rating,
                    COUNT(*)              AS review_count
                FROM review
                GROUP BY product_id
            ) r
                ON r.product_id = p.product_id
            WHERE 1 = 1
        """

        params: list = []

        # ----- filters -----
        if category:
            sql += " AND p.category = %s"
            params.append(category)

        if search:
            sql += " AND LOWER(p.product) LIKE %s"
            params.append("%" + search.lower() + "%")

        if brand:
            # логічно використовується для electronics
            sql += " AND e.brand = %s"
            params.append(brand)

        if author:
            # логічно використовується для books
            sql += " AND b.author = %s"
            params.append(author)

        if size:
            # логічно використовується для clothing
            sql += " AND cl.size = %s"
            params.append(size)

        # ORDER BY можна не робити (ми сортуємо у product_list),
        # але якщо хочеш – можна додати просте сортування по id:
        # sql += " ORDER BY p.product_id ASC"

        rows = self.storage.fetch_all(sql, params)
        return rows

    def get_products_filtered(
            self,
            *,
            search: str = "",
            category: str = "",
            brand: str = "",
            author: str = "",
            size: str = "",
            sort: str = "id",
            direction: str = "asc",
    ) -> list[dict]:
        """
        Load products from v_prod with optional filters.
        All rows already contain avg_rating and review_count.
        """
        sql = """
            SELECT
                product_id,
                product,
                price,
                weight,
                category,
                brand,
                warranty_years,
                size,
                author,
                page_count,
                avg_rating,
                review_count
            FROM v_prod
            WHERE 1 = 1
        """

        params: list = []

        if category:
            sql += " AND category = %s"
            params.append(category)

        if search:
            sql += " AND LOWER(product) LIKE %s"
            params.append("%" + search.lower() + "%")

        if brand:
            sql += " AND brand = %s"
            params.append(brand)

        if author:
            sql += " AND author = %s"
            params.append(author)

        if size:
            sql += " AND size = %s"
            params.append(size)

        # сортування залишаємо в Python (product_list), тут ORDER BY не потрібен
        rows = self.storage.fetch_all(sql, params)
        return rows

    def close(self):
        self.storage.disconnect()



# Test
if __name__ == "__main__":
    products = ProductMethods()
    products.get_all_products()
    products.get_product(12)
    products.get_product(1)
    products.close()
