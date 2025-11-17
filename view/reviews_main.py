from reviews.review_methods import ReviewMethods
from utils.input_helpers import get_int_input, optional_input, pause


def get_float_input(prompt: str) -> float:
    """Запит числа з плаваючою комою (rating, max price тощо)."""
    while True:
        value_str = input(prompt).strip().replace(",", ".")
        try:
            return float(value_str)
        except ValueError:
            print("Value must be a number (e.g. 4.5). Try again.")


def run_review_management() -> None:
    rm = ReviewMethods()

    while True:
        print("\n====================")
        print(" REVIEW MANAGEMENT ")
        print("1) Create review")
        print("2) Show reviews for product")
        print("3) Show rating summary for product")
        print("4) Show reviews for customer")
        print("5) Show rating summary for customer")
        print("6) Delete review")
        print("0) Back to main menu")

        choice = input("Select option: ").strip()

        match choice:
            case "1":
                print("\n--- Create review ---")
                customer_id = get_int_input("Customer ID: ")
                product_id = get_int_input("Product ID: ")
                rating = get_float_input("Rating (1–5): ")
                comment = optional_input("Comment (blank = no comment): ") or ""

                rm.save_review(
                    customer_id=customer_id,
                    product_id=product_id,
                    rating=rating,
                    comment=comment,
                )
                pause()

            case "2":
                print("\n--- Show reviews for product ---")
                product_id = get_int_input("Product ID: ")
                rm.get_reviews_for_product(product_id)
                pause()

            case "3":
                print("\n--- Rating summary for product ---")
                product_id = get_int_input("Product ID: ")
                rm.get_rating_summary_for_product(product_id)
                pause()

            case "4":
                print("\n--- Show reviews for customer ---")
                customer_id = get_int_input("Customer ID: ")
                rm.get_reviews_for_customer(customer_id)
                pause()

            case "5":
                print("\n--- Rating summary for customer ---")
                customer_id = get_int_input("Customer ID: ")
                rm.get_rating_summary_for_customer(customer_id)
                pause()

            case "6":
                print("\n--- Delete review ---")
                review_id = get_int_input("Review ID: ")
                rm.delete_review(review_id)
                pause()

            case "0":
                print("Back to main menu...")
                break

            case _:
                print("Invalid option, try again.")
                pause()

    rm.close()


if __name__ == "__main__":
    run_review_management()
