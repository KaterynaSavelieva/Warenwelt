# orders/order.py
from datetime import datetime
from pathlib import Path
from orders.shopping_cart import ShoppingCart

class Order:
    def __init__(self, cart: ShoppingCart, is_company: bool = False):
        self.order_time = datetime.now()

        #ЗНІМОК позицій
        # Підтримує як (product_id, qty), так і розширені кортежі
        self.ordered_products = [tuple(item) for item in list(cart.products)]

        self.user_id = cart.customer_id
        self.is_company = is_company

        # суму беремо зі знімка cart.total_sum (вже пораховано раніше)
        self.total_amount = float(cart.total_sum)
        if self.is_company:
            self.total_amount *= 0.95

        self.order_id: int | None = None

    def set_order_id(self, order_id: int) -> None:
        self.order_id = int(order_id)

    def calculate_total(self) -> float:
        return round(self.total_amount, 2)

    def create_invoice(self, filename: str | None = None) -> str:
        out_dir = Path(__file__).resolve().parents[1] / "invoices"
        out_dir.mkdir(parents=True, exist_ok=True)

        ts = self.order_time.strftime("%Y-%m-%d_%H-%M-%S")
        if filename is None:
            filename = (f"invoice_order_{self.order_id}_{ts}.txt"
                        if self.order_id else f"invoice_{ts}.txt")
        filepath = out_dir / filename

        # Спробуємо підтягнути назву/ціну з БД для кращого інвойсу
        try:
            from products.product_methods import ProductMethods
            pm = ProductMethods()
        except Exception:
            pm = None  # якщо немає доступу — просто виведемо IDs

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"ORDER ID: {self.order_id if self.order_id else '-'}\n")
            f.write(f"Customer ID: {self.user_id}\n")
            f.write(f"Date: {self.order_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Company discount: {'5%' if self.is_company else '0%'}\n")
            f.write("=" * 60 + "\n")
            f.write("Products:\n")

            # ітеруємо по копії позицій
            for item in self.ordered_products:
                # підтримка формату (pid, qty) або (pid, qty, name, price, ...)
                pid = item[0]
                qty = item[1] if len(item) > 1 else 1

                name = None
                price = None
                if len(item) >= 4:
                    name = item[2]
                    price = float(item[3])
                elif pm is not None:
                    try:
                        row = pm.storage.fetch_one(
                            "SELECT product, price FROM product WHERE product_id=%s", (pid,)
                        )
                        if row:
                            name = row["product"]
                            price = float(row["price"])
                    except Exception:
                        pass

                if name is not None and price is not None:
                    f.write(f"  [{pid}] {name} | Qty: {qty} | Price: {price:.2f} EUR\n")
                else:
                    f.write(f"  Product ID: {pid} | Quantity: {qty}\n")

            f.write("=" * 60 + "\n")
            f.write(f"Total amount: {self.calculate_total():.2f} EUR\n")

        # акуратно закриємо конекшн до продуктів, якщо відкривали
        try:
            if pm is not None:
                pm.close()
        except Exception:
            pass

        return str(filepath)
