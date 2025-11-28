from tabulate import tabulate

from models.reviews.review_methods import ReviewMethods
from utils.input_helpers import get_int_input, optional_input, pause, get_float_input


def run_review_management() -> None:
    """
    Console menu for managing reviews.
    Uses ReviewMethods for all DB operations.
    """
    rm = ReviewMethods()

    try:
        while True:
            print("\n====================")
            print(" REVIEW MANAGEMENT ")
            print("1) Show all reviews")
            print("2) Create review")
            print("3) Show reviews for product")
            print("4) Show rating summary for product")
            print("5) Show reviews for customer")
            print("6) Show rating summary for customer")
            print("7) Delete review")
            print("0) Back to main menu")

            choice = input("Select option: ").strip()

            match choice:
                # 1) All reviews
                case "1":
                    print("\n--- All reviews ---")
                    rows = rm.get_all_reviews()
                    if not rows:
                        print("No reviews in the system yet.")
                    else:
                        print(tabulate(rows, headers="keys", tablefmt="rounded_grid"))
                    pause()

                # 2) Create review
                case "2":
                    print("\n--- Create review ---")
                    customer_id = get_int_input("Customer ID: ")
                    product_id = get_int_input("Product ID: ")
                    rating = get_float_input("Rating (1–5): ")
                    comment = optional_input("Comment (blank = no comment): ") or ""

                    ok = rm.create_review(
                        customer_id=customer_id,
                        product_id=product_id,
                        rating=rating,
                        comment=comment,
                    )
                    if ok:
                        print("Review created successfully.")
                    else:
                        print("Review was not created.")
                    pause()

                # 3) Reviews for product
                case "3":
                    print("\n--- Show reviews for product ---")
                    product_id = get_int_input("Product ID: ")
                    rm.get_reviews_for_product(product_id)
                    pause()

                # 4) Rating summary for product
                case "4":
                    print("\n--- Rating summary for product ---")
                    product_id = get_int_input("Product ID: ")
                    rm.get_rating_summary_for_product(product_id)
                    pause()

                # 5) Reviews for customer
                case "5":
                    print("\n--- Show reviews for customer ---")
                    customer_id = get_int_input("Customer ID: ")
                    rm.get_reviews_for_customer(customer_id)
                    pause()

                # 6) Rating summary for customer
                case "6":
                    print("\n--- Rating summary for customer ---")
                    customer_id = get_int_input("Customer ID: ")
                    rm.get_rating_summary_for_customer(customer_id)
                    pause()

                # 7) Delete review
                case "7":
                    print("\n--- Delete review ---")
                    while True:
                        review_id = get_int_input("Enter the review ID you want to delete (0 to cancel): ")

                        if review_id == 0:
                            print("Deletion cancelled.")
                            break

                        row=rm.get_review(review_id)
                        if not row:
                            print("No such review. Try again.")
                            continue

                        confirm = input(f"Do you really want to delete ID {review_id}? [Y/N]: ").strip().lower()

                        if  confirm == "y":
                            rm.delete_review(review_id)
                        else:
                            print("Deletion cancelled.")
                        pause()
                    continue

                # 0) Exit to main menu
                case "0":
                    print("Back to main menu...")
                    break

                # Invalid choice
                case _:
                    print("Invalid option, please try again.")
                    pause()
    finally:
        # always close storage connection
        rm.close()


if __name__ == "__main__":
    run_review_management()
