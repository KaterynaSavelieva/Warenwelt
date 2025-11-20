from collections import Counter
from orders.shopping_cart import ShoppingCart

import os
from connection.storage import Storage
from datetime import datetime


class Order:
    def __init__(self, cart: ShoppingCart, is_company: bool = False):
        """
        Take a ShoppingCart and create a snapshot for the invoice:
        - customer_id
        - total_sum
        - list of (product_id, quantity)
        """
        self.customer_id: int | None = cart.customer_id
        self.is_company: bool = is_company
        self.total_sum: float = float(getattr(cart, "total_sum", 0.0))
        self.order_id: int | None = None

        ordered: list[tuple[int, int]] = []
        products = cart.products

        # cart.products can be:
        # - dict: {product_id: quantity}
        # - list of (product_id, quantity)
        # - list of product_id (repeated for quantity)
        if isinstance(products, dict):
            for pid, qty in products.items():
                pid = int(pid)
                qty = int(qty)
                if qty > 0:
                    ordered.append((pid, qty))

        elif isinstance(products, list) and products:
            first = products[0]

            if isinstance(first, (tuple, list)) and len(first) == 2:
                # e.g. [(1, 2), (3, 1)]
                for pid, qty in products:
                    pid = int(pid)
                    qty = int(qty)
                    if qty > 0:
                        ordered.append((pid, qty))
            else:
                # e.g. [1, 1, 2, 10, 10]  → compress with Counter
                counts = Counter(products)
                for pid, qty in counts.items():
                    pid = int(pid)
                    qty = int(qty)
                    if qty > 0:
                        ordered.append((pid, qty))
        else:
            # empty or unknown format
            ordered = []

        self.ordered_products: list[tuple[int, int]] = ordered

    def set_order_id(self, order_id: int | None) -> None:
        #Set the order ID after saving to the database.
        self.order_id = order_id

    def create_invoice(self) -> str:
        """
        Create a simple TXT invoice file in the 'invoices' folder
        and return the absolute path to the file.
        """
        if self.order_id is None:
            raise ValueError("order_id is not set for this order.")

        # 1) Make sure the invoices directory exists
        base_dir = os.path.dirname(os.path.dirname(__file__))  # project root
        invoices_dir = os.path.join(base_dir, "invoices")
        os.makedirs(invoices_dir, exist_ok=True)

        # 2) Create filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"invoice_order_{self.order_id}_{timestamp}.txt"
        full_path = os.path.join(invoices_dir, filename)

        # 3) Load product data from database
        storage = Storage()
        storage.connect()

        lines: list[str] = []
        lines.append(f"INVOICE #{self.order_id}")
        lines.append(f"Customer ID: {self.customer_id}")
        lines.append("")
        lines.append("Items:")

        total = 0.0

        for product_id, quantity in self.ordered_products:
            row = storage.fetch_one(
                "SELECT product, price FROM product WHERE product_id = %s",
                (product_id,),
            )
            if not row:
                continue

            name = row["product"]
            price = float(row["price"])
            line_total = price * quantity
            total += line_total

            lines.append(
                f"- {product_id}: {name} | qty: {quantity} | "
                f"price: {price:.2f} EUR | line total: {line_total:.2f} EUR"
            )

        storage.disconnect()

        lines.append("")
        if self.is_company:
            lines.append("Customer type: COMPANY (5% discount applied in order total).")
        else:
            lines.append("Customer type: PRIVATE.")

        lines.append(f"Order total (cart): {self.total_sum:.2f} EUR")
        lines.append(f"Order ID (DB): {self.order_id}")

        # 4) Write file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Invoice created: {full_path}")
        return full_path