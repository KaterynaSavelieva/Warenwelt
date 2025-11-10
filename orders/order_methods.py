from connection.storage import Storage
import pymysql

class OrderMethods:
    def __init__(self):
        # Create a connection to the database
        self.storage = Storage()
        self.storage.connect()

    def save_order(self, cart, is_company=False) -> int | None:
        """
        Saves an order into two tables:
        - 'bestellung' (order header)
        - 'bestellung_details' (order items)
        """
        try:
            # Check if the cart is empty
            if not cart.products:
                print("Cart is empty.")
                return None

            total = 0.0                 # total amount of the order
            items = []                  # will store (product_id, quantity, price)

            # Get product prices from the database
            for product_id, quantity in cart.products:
                # Get the product price by ID
                row = self.storage.fetch_one(
                    "SELECT price FROM product WHERE product_id=%s", (product_id,)
                )

                # If product not found, skip it
                if not row:
                    print(f"Product {product_id} not found. Skipped.")
                    continue

                price = float(row["price"])   # convert price to float
                items.append((product_id, quantity, price))
                total += price * quantity           # add to total

            # If no valid products were found
            if not items:
                print("No valid products to save.")
                return None

            # Apply company discount if needed
            if is_company:
                total *= 0.95  # 5% discount for company orders

            # Start a single database transaction
            self.storage.connection.begin()

            # Save main order record (header)
            order_id = self.storage.insert_and_get_id(
                "INSERT INTO bestellung (customer_id, total) VALUES (%s, %s)",
                (cart.customer_id, round(total, 2))
            )

            # If no ID was returned, something went wrong
            if not order_id:
                raise RuntimeError("Insert failed: no new order ID returned.")

            # 4.2 Save each product from the cart into bestellung_details
            sql_detail = """
                INSERT INTO bestellung_details (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            for product_id, quantity, price in items:
                self.storage.execute(sql_detail, (order_id, product_id, quantity, price))

            # Commit the transaction
            self.storage.connection.commit()
            print(f"Order saved successfully (ID {order_id})")

            #  Empty the cart after saving
            if hasattr(cart, "clear_cart"):
                cart.clear_cart()

            return order_id

        # Error handling
        except pymysql.err.IntegrityError as e:
            # For example, if foreign key constraint fails
            self.storage.connection.rollback()
            print("Integrity error while saving order:", e)
            return None

        except Exception as e:
            self.storage.connection.rollback()  # For all other unexpected errors
            print("Error while saving the order:", e)
            return None

    def close(self): # Close the database connection
        self.storage.disconnect()
