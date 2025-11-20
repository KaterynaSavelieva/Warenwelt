from collections import Counter
from orders.shopping_cart import ShoppingCart

import os
from connection.storage import Storage
from datetime import datetime
from pathlib import Path



class Order:
    def __init__(self, cart: ShoppingCart, is_company: bool = False):
        """
        Take a ShoppingCart and create a snapshot for the invoice:
        - customer_id
        - total_sum
        - list of (product_id, quantity)
        """
        self.cart = cart
        self.customer_id: int | None = cart.customer_id
        self.is_company: bool = is_company
        self.total_sum: float = float(getattr(cart, "total_sum", 0.0))
        self.order_id: int | None = None

        self.storage = Storage()
        self.storage.connect()

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
        Створює TXT-інвойс із:
          - даними клієнта (ім'я, тип, адреса, email, телефон)
          - таблицею куплених товарів (ID, Name, Qty, Price, Total)
          - підсумком, знижкою для company і total.
        """

        # 1) Дані клієнта
        customer = self.storage.fetch_one(
            """
            SELECT customer_id, name, email, address, phone, kind
            FROM customers
            WHERE customer_id = %s
            """,
            (self.cart.customer_id,),
        )

        # 2) Рядки замовлення по цьому order_id
        items = self.storage.fetch_all(
            """
            SELECT d.product_id,
                   p.product,
                   d.quantity,
                   d.price
            FROM order_items d
            JOIN product p ON p.product_id = d.product_id
            WHERE d.order_id = %s
            """,
            (self.order_id,),
        )

        # 2.1) Рахуємо subtotal і суму по кожному рядку
        subtotal = 0.0
        for row in items:
            line_total = float(row["price"]) * row["quantity"]
            row["line_total"] = line_total
            subtotal += line_total

        # 3) Знижка для компанії
        if self.is_company:
            discount = round(subtotal * 0.05, 2)
        else:
            discount = 0.0

        total = round(subtotal - discount, 2)

        # 4) Формуємо текст інвойсу
        now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
        kind_str = "COMPANY" if self.is_company else "PRIVATE"

        lines: list[str] = []
        lines.append(f"INVOICE #{self.order_id}")
        lines.append("")

        # ---- Блок КЛІЄНТ ----
        lines.append("Customer")
        lines.append("--------")
        if customer:
            lines.append(f"  Name   : {customer['name']}")
            lines.append(f"  ID     : {customer['customer_id']}")
            lines.append(f"  Type   : {kind_str}")
            lines.append(f"  Address: {customer.get('address') or '-'}")
            lines.append(f"  Email  : {customer.get('email') or '-'}")
            lines.append(f"  Phone  : {customer.get('phone') or '-'}")
        else:
            # запасний варіант, якщо раптом не знайдеться
            lines.append(f"  ID   : {self.cart.customer_id}")
            lines.append(f"  Type : {kind_str}")
        lines.append("")
        lines.append(f"Order date : {now_str}")
        lines.append("")

        # ---- Таблиця ТОВАРІВ ----
        header = f"{'ID':<4} {'Name':<30} {'Qty':>5} {'Price':>10} {'Total':>10}"
        lines.append("Items")
        lines.append("-----")
        lines.append(header)
        lines.append("-" * len(header))

        for row in items:
            pid = row["product_id"]
            name = row["product"]
            qty = row["quantity"]
            price = float(row["price"])
            line_total = row["line_total"]

            # .30 обрізає дуже довгі назви, щоб таблиця не “роз’їжджалась”
            lines.append(
                f"{pid:<4} {name:<30.30} {qty:>5} {price:>10.2f} {line_total:>10.2f}"
            )

        lines.append("")
        lines.append(f"{'Subtotal:':>53} {subtotal:>10.2f}")
        if discount > 0:
            lines.append(f"{'Company discount (5 %):':>53} -{discount:>9.2f}")
        lines.append(f"{'Total:':>53} {total:>10.2f}")
        lines.append("")

        # 5) Запис у файл
        invoices_dir = Path("invoices")
        invoices_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"invoice_order_{self.order_id}_{ts}.txt"
        full_path = invoices_dir / filename

        full_path.write_text("\n".join(lines), encoding="utf-8")

        # Можна закрити з'єднання (якщо цей об'єкт більше не потрібен)
        self.storage.disconnect()

        return str(full_path)
