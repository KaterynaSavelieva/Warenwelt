from connection.storage import Storage
from orders.shopping_cart import ShoppingCart
import pymysql


class OrderMethods:
    def __init__(self):
        self.storage = Storage()
        self.storage.connect()

    def save_order(self, cart: ShoppingCart, is_company: bool = False) -> int | None:
        """
        Saves an order into two tables:
        - 'bestellung' (order header)
        - 'bestellung_details' (order items)
        """
        try:
            # 1) basic checks
            if not cart.products:
                print("SAVE_ORDER: Cart is empty.")
                return None

            if cart.customer_id is None:
                print("SAVE_ORDER: customer_id is None.")
                return None

            total = 0.0
            items: list[tuple[int, int, float]] = []  # (product_id, quantity, price)

            # 2) normalize cart.products (support dict, tuples AND dicts)
            raw = cart.products

            # Example structures we support:
            # - {2: 1, 4: 3}
            # - [(2, 1), (4, 3)]
            # - [{"product_id": 2, "quantity": 1}, ...]
            if isinstance(raw, dict):
                # dict {product_id: qty}
                iterable = [(pid, qty) for pid, qty in raw.items()]
            else:
                # already some kind of list/tuple
                iterable = raw

            for entry in iterable:
                product_id = None
                quantity = 0

                if isinstance(entry, dict):
                    product_id = entry.get("product_id")
                    quantity = entry.get("quantity", 0)

                elif isinstance(entry, (tuple, list)) and len(entry) >= 2:
                    product_id = entry[0]
                    quantity = entry[1]

                else:
                    print(f"SAVE_ORDER: invalid cart item format {entry}, skipped.")
                    continue

                if not product_id or quantity <= 0:
                    print(f"SAVE_ORDER: invalid cart item {entry}, skipped.")
                    continue

                # 2.1) read current price from DB
                row = self.storage.fetch_one(
                    "SELECT price FROM product WHERE product_id = %s",
                    (product_id,),
                )

                if not row:
                    print(f"SAVE_ORDER: product {product_id} not found in DB, skipped.")
                    continue

                price = float(row["price"])
                items.append((product_id, quantity, price))
                total += price * quantity

            if not items:
                print("SAVE_ORDER: no valid products to save.")
                return None

            # 3) apply company discount if needed
            if is_company:
                total *= 0.95  # 5% discount

            total = round(total, 2)

            print(
                f"SAVE_ORDER: customer_id={cart.customer_id}, "
                f"is_company={is_company}, total={total}"
            )

            # 4) start transaction
            self.storage.connection.begin()

            # 4.1 insert into bestellung (order header)
            order_id = self.storage.insert_and_get_id(
                "INSERT INTO bestellung (customer_id, total) VALUES (%s, %s)",
                (cart.customer_id, total),
            )

            if not order_id:
                raise RuntimeError("SAVE_ORDER: insert into 'bestellung' returned no ID.")

            # 4.2 insert all items into bestellung_details
            sql_detail = """
                INSERT INTO bestellung_details (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            for product_id, quantity, price in items:
                self.storage.execute(sql_detail, (order_id, product_id, quantity, price))

            # 5) commit
            self.storage.connection.commit()
            print(f"SAVE_ORDER: order saved successfully (ID {order_id}).")

            # 6) optional: clear cart
            if hasattr(cart, "clear_cart"):
                cart.clear_cart()

            return order_id

        except pymysql.err.IntegrityError as e:
            self.storage.connection.rollback()
            print("SAVE_ORDER IntegrityError:", e)
            return None

        except pymysql.MySQLError as e:
            self.storage.connection.rollback()
            print("SAVE_ORDER MySQLError:", e)
            return None

        except Exception as e:
            self.storage.connection.rollback()
            print("SAVE_ORDER unexpected error:", e)
            return None

    def close(self):
        self.storage.disconnect()
