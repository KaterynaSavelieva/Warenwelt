from reviews.review_methods import ReviewMethods  # adjust path if needed

CUSTOMER_ID = 2
PRODUCT_ID = 3
RATING = 4.5
COMMENT = "Works great!"

def main() -> None:
    rm = ReviewMethods()
    try:
        # Show rating summaries before test
        rm.get_rating_summary_for_product(PRODUCT_ID)
        rm.get_rating_summary_for_customer(CUSTOMER_ID)

        # 1) Counts before
        before_prod = len(rm.get_reviews_for_product(PRODUCT_ID))
        before_cust = len(rm.get_reviews_for_customer(CUSTOMER_ID))

        # 2) Insert
        new_id = rm.save_review(
            customer_id=CUSTOMER_ID,
            product_id=PRODUCT_ID,
            rating=RATING,
            comment=COMMENT,
        )
        assert new_id, "Insert failed: no new review_id returned."

        # 3) Counts after insert
        after_prod = len(rm.get_reviews_for_product(PRODUCT_ID))
        after_cust = len(rm.get_reviews_for_customer(CUSTOMER_ID))
        assert after_prod >= before_prod + 1, "Product reviews count did not increase."
        assert after_cust >= before_cust + 1, "Customer reviews count did not increase."

        rm.get_rating_summary_for_product(PRODUCT_ID)
        rm.get_rating_summary_for_customer(CUSTOMER_ID)

        # 4) Delete
        assert rm.delete_review(new_id), "Delete failed."

        # 5) Counts after delete (should return to previous numbers or less)
        final_prod = len(rm.get_reviews_for_product(PRODUCT_ID))
        final_cust = len(rm.get_reviews_for_customer(CUSTOMER_ID))
        assert final_prod <= after_prod - 1, "Product reviews count did not decrease."
        assert final_cust <= after_cust - 1, "Customer reviews count did not decrease."

        # Show rating summaries after test
        rm.get_rating_summary_for_product(PRODUCT_ID)
        rm.get_rating_summary_for_customer(CUSTOMER_ID)

        print("\nTEST PASSED")
    finally:
        rm.close()

if __name__ == "__main__":
    main()
