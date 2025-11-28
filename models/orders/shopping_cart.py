from tabulate import tabulate
from models.products.product_methods import ProductMethods


class ShoppingCart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.products: dict[int, int] = {}   # {product_id: quantity}
        self.total_sum = 0.0
        self.is_company = False              # auto-detected later

    def add_product(self, product_id: int, quantity: int = 1):
        if quantity < 1:
            print("Quantity must be at least 1.")
            return

        self.products[product_id] = self.products.get(product_id, 0) + quantity
        print(f"Product {product_id} added (x{quantity}). Current quantity: {self.products[product_id]}")

    def remove_product(self, product_id: int):
        if product_id not in self.products:
            print(f"Product {product_id} not found in cart.")
            return

        del self.products[product_id]
        print(f"Product {product_id} removed.")

    def clear_cart(self):
        self.products.clear()
        self.total_sum = 0.0
        print("Shopping cart has been cleared.")

    def calculate_total_price(self, pm: ProductMethods) -> float:
        total = 0.0

        for product_id, qty in self.products.items():
            product = pm.get_product_basic(product_id)
            if not product:
                print(f"Warning: Product {product_id} not found in database!")
                continue

            total += float(product["price"]) * qty

        # company discount
        if self.is_company:
            total *= 0.95

        self.total_sum = round(total, 2)
        return self.total_sum

    def show_cart(self, pm: ProductMethods):
        if not self.products:
            print("Cart is empty.")
            return

        print("\n--- Shopping Cart ---")

        rows = []
        for pid, qty in self.products.items():
            p = pm.get_product_basic(pid)
            if not p:
                continue

            rows.append({
                "product_id": p["product_id"],
                "product": p["product"],
                "price": p["price"],
                "category": p["category"],
                "brand": p["brand"],
                "quantity": qty,
            })

        print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
        print(f"Total (last calculated) = {self.total_sum:.2f} EUR")
