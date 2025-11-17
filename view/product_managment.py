from products.product_methods import ProductMethods
from utils.input_helpers import (
    optional_input,
    get_int_input,
    pause,
)


def get_float_input(prompt: str) -> float:
    """Простий helper: запитати число з плаваючою комою."""
    while True:
        value_str = input(prompt).strip().replace(",", ".")
        try:
            return float(value_str)
        except ValueError:
            print("Value must be a number (e.g. 19.99). Try again.")


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
                product_name = input("Product name: ").strip()
                price = get_float_input("Price: ")
                weight = get_float_input("Weight: ")

                category = input("Category (electronics/clothing/books): ").strip().lower()

                author = None
                page_count = None
                brand = None
                warranty_years = None
                size = None

                if category == "books":
                    author = input("Author: ").strip()
                    page_count = get_int_input("Page count: ")

                elif category == "electronics":
                    brand = input("Brand: ").strip()
                    warranty_years = get_int_input("Warranty years: ")

                elif category == "clothing":
                    size = input("Size (e.g. S, M, L, 38): ").strip()

                pm.save_product(
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
                pause()

            case "4":
                print("\n--- Update product ---")
                product_id = get_int_input("Product ID to update: ")

                name = optional_input("New product name (blank = skip): ")
                price_str = optional_input("New price (blank = skip): ")
                weight_str = optional_input("New weight (blank = skip): ")

                price = float(price_str.replace(",", ".")) if price_str else None
                weight = float(weight_str.replace(",", ".")) if weight_str else None

                pm.update_product(
                    product_id=product_id,
                    name=name or None,
                    price=price,
                    weight=weight,
                )
                pause()

            case "5":
                print("\n--- Delete product ---")
                product_id = get_int_input("Product ID to delete: ")
                pm.delete_product(product_id)
                pause()

            case "6":
                print("\n--- Find products by category ---")
                category = input("Category (electronics/clothing/books): ").strip().lower()
                pm.find_products_by_category(category)
                pause()

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
