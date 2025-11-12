from datetime import datetime
from orders.shopping_cart import ShoppingCart

class Order:
    def __init__(self, cart: ShoppingCart, is_company: bool = False):
        self.order_time = datetime.now() # save orders time
        self.ordered_products = cart.products # list of products from the cart
        self.user_id = cart.customer_id # save the customer id
        self.total_amount = float(cart.total_sum) # save total amount

        if is_company:
            self.total_amount *= 0.95 # give 5% discount if it is a company

    def calculate_total(self):
        return round(self.total_amount, 2) # round the total to 2 decimals

    def create_invoice(self, filename=None): #Create a simple text invoice with automatic unique name

        if filename is None:  # generate unique filename if not given
            timestamp = self.order_time.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"invoice_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Invoice for Customer ID: {self.user_id}\n")
            f.write(f"Date: {self.order_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n")
            f.write("Products:\n")

            # list all products
            for product_id, quantity in self.ordered_products:
                f.write(f" Product ID: {product_id} | Quantity: {quantity}\n")

            f.write("=" * 50 + "\n")
            f.write(f"Total amount: {self.calculate_total():.2f} EUR\n")

        print(f"Invoice saved as {filename}")
