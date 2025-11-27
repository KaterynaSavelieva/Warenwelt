from models.orders.shopping_cart import ShoppingCart
from models.orders.order_methods import OrderMethods
from models.products.product_methods import ProductMethods
from utils.input_helpers import get_int_input, pause

def run_order_management():
    pm = ProductMethods()
    om = OrderMethods()

    # тимчасовий кошик (одна сесія)
    cart = ShoppingCart(customer_id=0)

    print("\n--- Shopping cart / Order management ---")

    while True:
        print("\n====================")
        print(" SHOPPING CART / ORDER MANAGEMENT ")
        print("1) Set customer ID")
        print("2) Add product to cart")
        print("3) Remove product")
        print("4) Show cart")
        print("5) Calculate total")
        print("6) Save order")
        print("7) Create invoice")
        print("0) Back to main menu")

        choice = input("Select option: ").strip()

        match choice:

            case "1":
                cart.customer_id = get_int_input("Customer ID: ")

            case "2":
                pid = get_int_input("Product ID: ")
                qty = get_int_input("Quantity: ")
                cart.add_product(pid, qty)

            case "3":
                pid = get_int_input("Product ID to remove: ")
                cart.remove_product(pid)

            case "4":
                cart.show_cart()
                pause()

            case "5":
                total = cart.calculate_total_price(pm)
                print(f"Total = {total:.2f} EUR")
                pause()

            case "6":
                is_company = input("Company order? (y/n): ").strip().lower() == "y"
                order_id = om.save_order(cart, is_company)
                if order_id:
                    print(f"Order saved. ID = {order_id}")
                pause()

            case "7":
                from orders.order import Order
                order = Order(cart, is_company=False)
                print("Invoice file:", order.create_invoice())
                pause()

            case "0":
                print("Back to main menu...")
                om.close()
                pm.close()
                break

            case _:
                print("Invalid option, try again.")
                pause()
