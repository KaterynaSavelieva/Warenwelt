from products.product_methods import ProductMethods

class ShoppingCart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.products: dict[int, int] = {}   # {product_id: quantity}
        self.total_sum = 0.0


    def add_product(self, product_id: int, quantity: int = 1):
        if quantity < 1:
            print("Quantity must be at least 1.")
            return

        if product_id in self.products:
            self.products[product_id] += quantity
        else:
            self.products[product_id] = quantity

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


    def calculate_total_price(self, product_methods: ProductMethods) -> float:
        total = 0.0

        for product_id, quantity in self.products.items():
            product = product_methods.get_product(product_id)
            if not product:
                print(f"Warning: Product {product_id} not found in database!")
                continue

            total += float(product["price"]) * quantity

        self.total_sum = round(total, 2)
        return self.total_sum


    def show_cart(self):
        if not self.products:
            print("Cart is empty.")
            return

        print("\n--- Shopping Cart ---")
        for pid, qty in self.products.items():
            print(f"Product ID {pid}: quantity × {qty}")
        print(f"Total (no DB prices yet): {self.total_sum}")
