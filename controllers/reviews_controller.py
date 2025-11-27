from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.reviews.review_methods import ReviewMethods
from connection.storage import Storage

reviews_bp = Blueprint("reviews", __name__)

rm = ReviewMethods()

@reviews_bp.route("/reviews", methods=["GET", "POST"])
def reviews_view():
    """
    Reviews page:
      - GET: show filter form and list of all reviews (+ average rating per product).
      - POST: create a new review for a product the current customer has bought.
    """
    storage = Storage()
    storage.connect()

    customer_id = session.get("customer_id")
    error = None

    # ----- filter / sort parameters from URL -----
    search = (request.args.get("search") or "").strip()
    category_filter = request.args.get("category", "")
    rating_filter = request.args.get("rating", "")
    sort = request.args.get("sort", "date")
    direction = request.args.get("dir", "desc")

    # allowed sort fields
    sort_map = {
        "date": "r.created_at",
        "product": "p.product",
        "category": "p.category",
        "customer": "c.name",
        "rating": "r.rating",
        "comment": "r.comment",
        "avg_rating": "avg_rating",
    }
    sort_column = sort_map.get(sort, "r.created_at")
    dir_sql = "ASC" if direction == "asc" else "DESC"
    order_clause = f"{sort_column} {dir_sql}"

    # ----- POST: create new review -----
    if request.method == "POST":
        if not customer_id:
            flash("Please log in to write a review.", "error")
            storage.disconnect()
            return redirect(url_for("login"))

        try:
            product_id = int(request.form.get("product_id", "0"))
        except ValueError:
            product_id = 0

        try:
            rating = int(request.form.get("rating", "0"))
        except ValueError:
            rating = 0

        comment = (request.form.get("comment") or "").strip()

        # check if customer really bought this product
        allowed = storage.fetch_one(
            """
            SELECT 1
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.customer_id = %s
              AND oi.product_id = %s
            LIMIT 1
            """,
            (customer_id, product_id),
        )

        if not allowed:
            error = "You can review only products you have bought."
        elif rating < 1 or rating > 5:
            error = "Rating must be between 1 and 5."
        else:
            storage.execute(
                """
                INSERT INTO review (customer_id, product_id, rating, comment)
                VALUES (%s, %s, %s, %s)
                """,
                (customer_id, product_id, rating, comment),
            )
            storage.connection.commit()
            flash("Thank you for your review!", "success")
            storage.disconnect()
            # after successful insert, redirect back to GET with same filters
            return redirect(
                url_for(
                    "reviews.reviews_view",
                    search=search,
                    category=category_filter,
                    rating=rating_filter,
                    sort=sort,
                    dir=direction,
                )
            )

    # ----- 1) load all reviews with filters and sorting -----
    where_clauses = []
    params: list = []

    if search:
        where_clauses.append(
            "(p.product LIKE %s OR c.name LIKE %s OR r.comment LIKE %s)"
        )
        like = f"%{search}%"
        params.extend([like, like, like])

    if category_filter:
        where_clauses.append("p.category = %s")
        params.append(category_filter)

    if rating_filter:
        where_clauses.append("r.rating = %s")
        params.append(int(rating_filter))

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    sql = f"""
        SELECT
            r.review_id,
            r.rating,
            r.comment,
            r.created_at,
            c.name       AS customer_name,
            p.product_id,
            p.product    AS product_name,
            p.category   AS category,
            ar.avg_rating,
            ar.review_count
        FROM review r
        JOIN customers c ON c.customer_id = r.customer_id
        JOIN product   p ON p.product_id   = r.product_id
        LEFT JOIN (
            SELECT
                product_id,
                AVG(rating) AS avg_rating,
                COUNT(*)    AS review_count
            FROM review
            GROUP BY product_id
        ) ar ON ar.product_id = p.product_id
        {where_sql}
        ORDER BY {order_clause}
    """

    all_reviews = storage.fetch_all(sql, tuple(params))

    # ----- 2) products that current customer can still review -----
    purchasable_products = []
    if customer_id:
        purchasable_products = storage.fetch_all(
            """
            SELECT DISTINCT
                p.product_id,
                p.product  AS product_name
            FROM orders o
            JOIN order_items oi ON oi.order_id   = o.order_id
            JOIN product     p  ON p.product_id  = oi.product_id
            LEFT JOIN review r
                   ON r.customer_id = o.customer_id
                  AND r.product_id  = p.product_id
            WHERE o.customer_id = %s
              AND r.review_id IS NULL
            ORDER BY p.product_id
            """,
            (customer_id,),
        )

    # ----- 3) list of categories for filter dropdown -----
    categories = storage.fetch_all(
        "SELECT DISTINCT category FROM product ORDER BY category"
    )

    storage.disconnect()

    return render_template(
        "reviews.html",
        reviews=all_reviews,
        purchasable_products=purchasable_products,
        categories=categories,
        error=error,
        search=search,
        category_filter=category_filter,
        rating_filter=rating_filter,
        sort=sort,
        direction=direction,
    )

