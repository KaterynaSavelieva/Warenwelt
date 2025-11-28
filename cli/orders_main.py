from models.orders.shopping_cart import ShoppingCart
from models.orders.order_methods import OrderMethods
from models.customers.customer_methods import CustomerMethods
from models.orders.order import Order
from models.products.product_methods import ProductMethods
from utils.input_helpers import get_int_input, pause


def run_order_management() -> None:
    pm = ProductMethods()
    om = OrderMethods()
    cm = CustomerMethods()


    cart = ShoppingCart(customer_id=0)

    print("\n--- ORDER MANAGEMENT ---")

    while True:
        print("\n====================")
        print(" ORDER MANAGEMENT ")
        print("1) Create new order")
        print("2) Edit current order")
        print("3) Show cart")
        print("4) Calculate total")gi
        print("5) Save order")
        print("6) Create invoice")
        print("0) Back to main menu")

        choice = input("Select option: ").strip()

        match choice:

            case "1":
                print("\n--- CREATE NEW ORDER ---")

                cart.clear_cart()

                # Set customer ID
                while True:
                    customer_id = get_int_input("Customer ID: ")
                    customer = cm.get_customer(customer_id)
                    if customer:
                        cart.customer_id = customer_id
                        break
                    print("Invalid customer ID. Try again.")

                # Auto-detect company / private
                cart.is_company = (customer["kind"] == "company")

                print(f"Customer: {customer['name']} ({customer['kind']})")

                # Fill cart
                print("\nEnter products (0 = finish):")
                while True:
                    pid = get_int_input("Product ID: ")
                    if pid == 0:
                        break

                    qty = get_int_input("Quantity: ")
                    cart.add_product(pid, qty)

                # Show result
                cart.show_cart(pm)
                pause()


            case "2":
                print("\n--- EDIT CURRENT ORDER ---")
                print("a) Add product")
                print("b) Remove product")
                print("c) Clear cart")
                print("x) Back")

                sub = input("Select: ").strip().lower()

                if sub == "a":
                    pid = get_int_input("Product ID: ")
                    qty = get_int_input("Quantity: ")
                    cart.add_product(pid, qty)

                elif sub == "b":
                    pid = get_int_input("Product ID to remove: ")
                    cart.remove_product(pid)

                elif sub == "c":
                    cart.clear_cart()

                pause()


            case "3":
                cart.show_cart(pm)
                pause()


            case "4":
                total = cart.calculate_total_price(pm)
                print(f"Total = {total:.2f} EUR")
                pause()


            case "5":
                if not cart.products:
                    print("Cart is empty.")
                    pause()
                    continue

                total = cart.calculate_total_price(pm)
                print(f"Calculated total: {total:.2f} EUR")

                confirm = input("Save this order? (y/n): ").strip().lower()
                if confirm != "y":
                    print("Order cancelled.")
                    pause()
                    continue

                order_id = om.save_order(cart, cart.is_company)
                if order_id:
                    print(f"Order saved! ID = {order_id}")

                pause()


            case "6":
                if not cart.products:
                    print("Cart is empty.")
                    pause()
                    continue

                order = Order(cart, is_company=cart.is_company)
                fname = order.create_invoice()
                print("Invoice created:", fname)
                pause()


            case "0":
                om.close()
                pm.close()
                print("Back to main menu...")
                break

            case _:
                print("Invalid option. Try again.")
                pause()
