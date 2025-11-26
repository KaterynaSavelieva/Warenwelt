from cli.customers_management import run_customer_management
from cli.product_managment import run_product_management
from cli.reviews_main import run_review_management
from utils.input_helpers import pause
from cli.orders_main import run_order_management


def main() -> None:
    while True:
        print("\n====================")
        print(" MAIN MENU ")
        print("1) Customer management")
        print("2) Product management")
        print("3) Review management")
        print("4) Shopping cart / Order management")
        print("0) Exit")

        choice = input("Select option: ").strip()

        match choice:
            case "1":
                run_customer_management()

            case "2":
                run_product_management()

            case "3":
                run_review_management()

            case "4":
                run_order_management()

            case "0":
                print("Goodbye!")
                break

            case _:
                print("Invalid option, try again.")
                pause()


if __name__ == "__main__":
    main()
