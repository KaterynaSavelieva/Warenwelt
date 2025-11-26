from products.product_methods import ProductMethods
from utils.input_helpers import (
    optional_input,
    get_int_input,
    pause, get_optional_int_input, get_float_input, get_optional_float_input
)
from customers.validator import _Rules


def run_product_management() -> None:
    pm = ProductMethods()

    while True:
        print("\n====================")
        print(" PRODUCT MANAGEMENT (WARENWELT) ")
        print("1) Show all products")
        print("2) Show product by ID")
        print("3) Create product")
        print("4) Update product")
        print("5) Delete product")
        print("6) Find products by category")
        print("7) Find products under max price")
        print("0) Back / Exit")

        choice = input("Select option: ").strip()

        match choice:
            case "1":
                print("\n--- Show all products ---")
                pm.get_all_products()
                pause()

            case "2":
                print("\n--- Show product by ID ---")
                product_id = get_int_input("Product ID: ")
                pm.get_product(product_id)
                pause()

            case "3":
                print("\n--- Create product ---")
                product_name = _Rules.clean_text_fields(input("Product name: "))
                price = get_float_input("Price: ")
                weight = get_float_input("Weight: ")

                category = _Rules.clean_text_fields(input("Category (electronics/clothing/books): ")).lower()

                author = None
                page_count = None
                brand = None
                warranty_years = None
                size = None

                if category == "books":
                    author = _Rules.clean_text_fields(input("Author: ").title())
                    page_count = get_optional_int_input("Page count (blank = skip): ")

                elif category == "electronics":
                    brand = _Rules.clean_text_fields(input("Brand: ").title())
                    warranty_years = get_int_input("Warranty years: ")

                elif category == "clothing":
                    size = input("Size (e.g. S, M, L, 38): ").strip()

                new_id = pm.save_product(
                    product_new=product_name,
                    price=price,
                    weight=weight,
                    category=category,
                    author=author,
                    page_count=page_count,
                    brand=brand,
                    warranty_years=warranty_years,
                    size=size,
                )
                pm.get_product(new_id)
                pause()


            case "4":
                print("\n--- Update product ---")
                product_id = get_int_input("Product ID to update: ")

                raw_name = optional_input("New product name (blank = skip): ")
                name = raw_name.title() if raw_name else None
                price = get_optional_float_input("New price (blank = skip): ")
                weight = get_optional_float_input("New weight (blank = skip): ")

                pm.update_product(
                    product_id=product_id,
                    name=name,
                    price=price,
                    weight=weight,
                )
                pm.get_product(product_id)
                pause()


            case "5":
                print("\n--- Delete product ---")
                product_id = get_int_input("Product ID to delete: ")
                row= pm.get_product(product_id)

                if not row:
                    print("\n--- No such product ---")
                    pause()
                    continue


                name = row ["product"]

                confirm = input(f"Do you really want to delete '{name}' (ID {product_id})? [Y/N]: ").strip().lower()

                if confirm == "y":
                    pm.delete_product(product_id)
                else:
                    print("Deletion cancelled.")

                pause()

            case "6":
                print("\n--- Find products by category ---")

                while True:
                    print("\n Choose category: ")
                    print("1 - Electronics")
                    print("2 - Clothing")
                    print("3 - Books")
                    print("0 - Back / Exit")

                    choice = input("Select option: ").strip()

                    if choice  == "0":
                        print("Back...")
                        pause()
                        break

                    categories = {
                        "1": "electronics",
                        "2": "clothing",
                        "3": "books"
                    }

                    if choice not in categories:
                        print("Invalid category. Enter 1–3 or 0 to exit.")
                        continue

                    category = categories[choice]

                    pm.find_products_by_category(category)

                    continue

            case "7":
                print("\n--- Find products under max price ---")
                max_price = get_float_input("Max price: ")
                pm.find_products_under_price(max_price)
                pause()

            case "0":
                print("Back / Exit...")
                break

            case _:
                print("Invalid option, try again.")
                pause()

    pm.close()


if __name__ == "__main__":
    run_product_management()
