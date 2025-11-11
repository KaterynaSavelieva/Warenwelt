from produсts.product_methods import ProductMethods
from orders.shopping_cart import ShoppingCart
from orders.order_methods import OrderMethods
from orders.order import Order

def main():
    #  helpers
    products = ProductMethods()     # gives us access to product queries
    cart = ShoppingCart(customer_id=2)  # a new empty cart for customer #2

    # Add products to the cart
    #    (product_id, quantity). If quantity is omitted, default = 1.
    cart.add_product(2, 25)

    cart.add_product(3, 101)

    # Calculate total price using current DB prices
    total = cart.calculate_total_price(products)
    print(f"Cart total (before discount): {total:.2f} EUR")

    # Save the order to the database (header + details)
    orders = OrderMethods()
    order_id = orders.save_order(cart, is_company=True)  # 5% discount for company

    if order_id:
        print(f"Order saved with ID: {order_id}")

        # Create a simple text invoice (auto name if you omit filename)
        order = Order(cart, is_company=True)
        order.create_invoice()  # e.g. invoice_2025-11-10_17-45-33.txt
    else:
        print("Order was not saved.")

    #  Close DB connections
    orders.close()
    products.close()

if __name__ == "__main__":
    main()
