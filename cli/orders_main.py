from models.orders.shopping_cart import ShoppingCart
from models.orders.order_methods import OrderMethods
from models.orders.order import Order
from models.products.product_methods import ProductMethods
from utils.input_helpers import get_int_input, pause


def run_order_management() -> None:
    """
    Simple console menu for working with shopping cart and orders.
    One temporary cart for the whole session.
    """

    pm = ProductMethods()
    om = OrderMethods()

    # temporary cart for one console session
    cart = ShoppingCart(customer_id=0)
    cart.is_company = False   # remember last choice for invoice

    print("\n--- Shopping cart / Order management ---")

    while True:
        print("\n====================")
        print(" SHOPPING CART / ORDER MANAGEMENT ")
        print("1) Set customer ID")
        print("2) Add product to cart")
        print("3) Remove product from cart")
        print("4) Show cart")
        print("5) Calculate total")
        print("6) Save order")
        print("7) Create invoice")
        print("0) Back to main menu")

        choice = input("Select option: ").strip()

        match choice:

            # 1) Set customer id
            case "1":
                cart.customer_id = get_int_input("Customer ID: ")

            # 2) Add product
            case "2":
                pid = get_int_input("Product ID: ")
                qty = get_int_input("Quantity: ")
                if qty <= 0:
                    print("Quantity must be greater than 0.")
                else:
                    cart.add_product(pid, qty)

            # 3) Remove product
            case "3":
                pid = get_int_input("Product ID to remove: ")
                cart.remove_product(pid)

            # 4) Show cart
            case "4":
                cart.show_cart()
                pause()

            # 5) Calculate total (no saving)
            case "5":
                total = cart.calculate_total_price(pm)
                print(f"Total = {total:.2f} EUR")
                pause()

            # 6) Save order to database
            case "6":
                # basic checks
                if cart.customer_id == 0:
                    print("Please set customer ID first (option 1).")
                    pause()
                    continue

                if not cart.items:
                    print("Cart is empty. Add products first (option 2).")
                    pause()
                    continue

                cart.is_company = input("Company order? (y/n): ").strip().lower() == "y"

                order_id = om.save_order(cart, cart.is_company)
                if order_id:
                    print(f"Order saved. ID = {order_id}")
                    # optional: clear cart after successful order
                    # cart.items.clear()
                else:
                    print("Order was not saved.")

                pause()

            # 7) Create invoice file for current cart
            case "7":
                if cart.customer_id == 0:
                    print("Please set customer ID first (option 1).")
                    pause()
                    continue

                if not cart.items:
                    print("Cart is empty. Add products first (option 2).")
                    pause()
                    continue

                # use last chosen flag (from case "6"), default = False
                is_company = getattr(cart, "is_company", False)

                order = Order(cart, is_company=is_company)
                filename = order.create_invoice()
                print("Invoice file created:", filename)
                pause()

            # 0) Exit submenu
            case "0":
                print("Back to main menu...")
                om.close()
                pm.close()
                break

            # wrong menu option
            case _:
                print("Invalid option, try again.")
                pause()
