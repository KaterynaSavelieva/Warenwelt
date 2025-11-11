from reviews.review_methods import ReviewMethods  # adjust path if needed

CUSTOMER_ID = 2
PRODUCT_ID = 3
RATING = 4.5
COMMENT = "Works great!"

def print_rows(title: str, rows: list[dict]):
    #Pretty print rows in a very simple way
    print(f"\n--- {title} (count={len(rows)}) ---")
    if not rows:
        print("(no rows)")
        return
    # print first 5 rows
    for i, r in enumerate(rows[:5], start=1):
        print(f"{i}. ", end="")
        for k, v in r.items():
            print(f"{k}={v}  ", end="")
        print()

def main():
    rm = ReviewMethods()

    try:
        # 1) Read initial lists
        before_prod = rm.get_reviews_for_product(PRODUCT_ID)
        before_cust = rm.get_reviews_for_customer(CUSTOMER_ID)
        print_rows("Before: product reviews", before_prod)
        print_rows("Before: customer reviews", before_cust)

        # 2) Insert a new review
        new_id = rm.save_review(
            customer_id=CUSTOMER_ID,
            product_id=PRODUCT_ID,
            rating=RATING,
            comment=COMMENT
        )
        if not new_id:
            print("Insert failed -> stop test.")
            return

        # 3) Check lists after insert
        after_prod = rm.get_reviews_for_product(PRODUCT_ID)
        after_cust = rm.get_reviews_for_customer(CUSTOMER_ID)
        print_rows("After insert: product reviews", after_prod)
        print_rows("After insert: customer reviews", after_cust)

        # very basic checks
        assert len(after_prod) >= len(before_prod) + 1, "Product reviews did not grow."
        assert len(after_cust) >= len(before_cust) + 1, "Customer reviews did not grow."

        # 4) Delete the review
        ok = rm.delete_review(new_id)
        assert ok, "Delete failed."

        # 5) Check lists after delete
        final_prod = rm.get_reviews_for_product(PRODUCT_ID)
        final_cust = rm.get_reviews_for_customer(CUSTOMER_ID)
        print_rows("After delete: product reviews", final_prod)
        print_rows("After delete: customer reviews", final_cust)

        # counts should be back to original (or at least not bigger)
        assert len(final_prod) <= len(after_prod) - 1, "Product reviews did not shrink."
        assert len(final_cust) <= len(after_cust) - 1, "Customer reviews did not shrink."

        print("\n TEST PASSED")
    finally:
        rm.close()

if __name__ == "__main__":
    main()
