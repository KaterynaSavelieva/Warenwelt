from customers.customer_methods import CustomerMethods
from utils.input_helpers import (
    optional_input,
    get_int_input,
    pause,
)


def run_customer_management() -> None:
    cm = CustomerMethods()

    while True:
        print("\n====================")
        print(" CUSTOMER MANAGEMENT ")
        print("1) Show all customers")
        print("2) Show customer by ID")
        print("3) Create customer")
        print("4) Update customer")
        print("5) Delete customer")
        print("6) Find customers by kind (private/company)")
        print("0) Back to main menu")

        choice = input("Select option: ").strip()

        match choice:
            case "1":
                print("\n--- Show all customers ---")
                cm.get_all_customers()
                pause()

            case "2":
                print("\n--- Show customer by ID ---")
                customer_id = get_int_input("Customer ID: ")
                cm.get_customer(customer_id)
                pause()

            case "3":
                print("\n--- Create customer ---")
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                kind = input("Kind (private/company): ").strip().lower()

                address = optional_input("Address (blank = skip): ")
                phone = optional_input("Phone (blank = skip): ")
                password = input("Password: ").strip()

                birthdate = None
                company_number = None

                if kind == "private":
                    birthdate = input("Birthdate (YYYY-MM-DD): ").strip()
                elif kind == "company":
                    company_number = input("Company number: ").strip()

                try:
                    cm.save_customer(
                        name=name,
                        email=email,
                        kind=kind,
                        address=address or None,
                        phone=phone or None,
                        password=password,
                        birthdate=birthdate or None,
                        company_number=company_number or None,
                    )
                except ValueError as e:
                    # коротке повідомлення з Validator / save_customer
                    print(f"Input error: {e}")

                pause()

            case "4":
                print("\n--- Update customer ---")
                customer_id = get_int_input("Customer ID: ")

                name = optional_input("New name (blank = skip): ")
                address = optional_input("New address (blank = skip): ")
                phone = optional_input("New phone (blank = skip): ")
                password = optional_input("New password (blank = skip): ")

                try:
                    cm.update_customer(
                        customer_id=customer_id,
                        name=name or None,
                        address=address or None,
                        phone=phone or None,
                        password=password or None,
                    )
                except ValueError as e:
                    print(f" Input error: {e}")

                pause()

            case "5":
                print("\n--- Delete customer ---")
                customer_id = get_int_input("Customer ID: ")
                cm.delete_customer(customer_id)
                pause()

            case "6":
                print("\n--- Find customers by kind ---")
                kind = input("Kind (private/company): ").strip().lower()
                try:
                    cm.find_customers_by_kind(kind)
                except ValueError as e:
                    print(f"Input error: {e}")
                pause()

            case "0":
                print("Back to main menu...")
                break

            case _:
                print("Invalid option, try again.")
                pause()

    cm.close()
