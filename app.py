from flask import Flask, render_template, request, redirect, url_for, session, flash
from products.product_methods import ProductMethods
from collections import Counter
from decimal import Decimal
from orders.shopping_cart import ShoppingCart
from orders.order import Order
from orders.order_methods import OrderMethods
from customers.customer_methods import CustomerMethods
from reviews.review_methods import ReviewMethods
from connection.storage import Storage
from customers.validator import Validator
from pydantic import ValidationError


app = Flask(__name__)
app.secret_key = "change_me_to_a_random_secret_key"


def eur(value):
    """
    Format number as European currency style "0 000,00".
    Used as Jinja filter.
    """
    if value is None:
        return "0,00"
    try:
        if isinstance(value, Decimal):
            value = float(value)
        else:
            value = float(value)
    except (TypeError, ValueError):
        return "0,00"

    s = f"{value:,.2f}"        # e.g. "16,199.82"
    s = s.replace(",", " ")    # "16 199.82"
    s = s.replace(".", ",")    # "16 199,82"
    return s


app.jinja_env.filters["eur"] = eur

# Single shared instances for this process
pm = ProductMethods()
cm = CustomerMethods()
rm = ReviewMethods()


# ====================== CART HELPERS (SESSION) ======================

def get_cart_ids() -> list[int]:
    """
    Read 'cart' list from session.
    Returns empty list if no cart is present.
    """
    return session.get("cart", [])


def add_to_cart(product_id: int) -> None:
    """
    Append product_id to the cart list in session.
    Cart is stored as a simple list of product_ids (may contain duplicates).
    """
    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart


def calculate_cart_total(products, counts: Counter) -> float:
    """
    Calculate total cart sum based on:
      - products: list of rows (must contain product_id and price)
      - counts: Counter(product_id -> quantity)
    """
    total = 0.0
    for p in products:
        pid = p["product_id"]
        qty = counts.get(pid, 0)
        if qty > 0:
            price_each = float(p["price"])
            total += qty * price_each
    return total


def check_password(user_row: dict, plain_password: str) -> bool:
    """
    Very simple password check:
    compares plain text from form with plain text stored in the database.
    (In a real project you would use hashed passwords!)
    """
    if not user_row:
        return False
    db_password = user_row.get("password")
    if db_password is None:
        return False
    return db_password == plain_password


# =========================== ROUTES ===========================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def product_list():
    view = request.args.get("view", "table")
    if view not in ("table", "cards"):
        view = "table"

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    brand = request.args.get("brand", "").strip()
    author = request.args.get("author", "").strip()
    size = request.args.get("size", "").strip()
    sort = request.args.get("sort", "id")
    direction = request.args.get("dir", "asc")

    # --- DEBUG (можеш увімкнути на час тестів) ---
    # print("DEBUG FILTERS:", search, category, brand, author, size, sort, direction)

    # Якщо обрана категорія, чистимо неактуальні фільтри,
    # щоб не було «перетину» brand+author+size
    if category == "electronics":
        author = ""
        size = ""
    elif category == "books":
        brand = ""
        size = ""
    elif category == "clothing":
        brand = ""
        author = ""
    # якщо category == "" – усе дозволено

    all_products = pm.get_all_products()

    cart_ids = get_cart_ids()
    counts = Counter(cart_ids)
    cart_total = calculate_cart_total(all_products, counts)

    categories = sorted({p["category"] for p in all_products})
    brands = sorted({p["brand"] for p in all_products if p.get("brand")})
    authors = sorted({p["author"] for p in all_products if p.get("author")})
    sizes = sorted({p["size"] for p in all_products if p.get("size")})

    products = pm.get_products_filtered(
        search=search,
        category=category,
        brand=brand,
        author=author,
        size=size,
    )

    def total_for(p):
        return counts.get(p["product_id"], 0) * float(p["price"])

    key_map = {
        "id":       lambda p: p["product_id"],
        "name":     lambda p: p["product"],
        "category": lambda p: p["category"],
        "price":    lambda p: float(p["price"]),
        "total":    total_for,
        "rating":   lambda p: float(p["avg_rating"] or 0.0),
    }
    key_func = key_map.get(sort, key_map["id"])
    reverse = (direction == "desc")
    products = sorted(products, key=key_func, reverse=reverse)

    return render_template(
        "products.html",
        products=products,
        view=view,
        search=search,
        category=category,
        brand=brand,
        author=author,
        size=size,
        sort=sort,
        direction=direction,
        cart_total=cart_total,
        counts=counts,
        categories=categories,
        brands=brands,
        authors=authors,
        sizes=sizes,
    )



@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart_route(product_id: int):
    """
    Handler for "Add to cart" button on products page.
    After adding, redirect back to the same place (row anchor),
    if return_url is provided.
    """
    add_to_cart(product_id)

    # спробуємо повернутися туди, звідки прийшов запит
    return_url = request.form.get("return_url")
    if return_url:
        return redirect(return_url)

    # fallback – як і було раніше
    view = request.args.get("cli", "table")
    if view not in ("table", "cards"):
        view = "table"

    return redirect(url_for("product_list", view=view))


@app.route("/set_cart_quantity/<int:product_id>", methods=["POST"])
def set_cart_quantity(product_id: int):
    """
    Set exact quantity for given product_id in session cart.
    Quantity is set by replacing all previous occurrences of this product_id.
    """
    cart = get_cart_ids()
    try:
        qty = int(request.form.get("qty", "0"))
    except ValueError:
        qty = 0

    if qty < 0:
        qty = 0

    # remove all old occurrences of this product_id
    cart = [pid for pid in cart if pid != product_id]
    # add product_id qty times
    cart.extend([product_id] * qty)
    session["cart"] = cart

    # redirect back to the same page (with anchor)
    return_url = request.form.get("return_url")
    if return_url:
        return redirect(return_url)

    return redirect(request.referrer or url_for("product_list"))


@app.route("/cart")
def cart_view():
    """
    Shows the shopping cart with:
      - quantities per product,
      - line totals,
      - global total.
    """
    cart_ids = get_cart_ids()
    counts = Counter(cart_ids)

    all_products = pm.get_all_products()

    cart_products = []
    cart_total = 0.0

    for p in all_products:
        pid = p["product_id"]
        qty = counts.get(pid, 0)
        if qty <= 0:
            continue

        price_each = float(p["price"])
        line_total = qty * price_each
        cart_total += line_total

        cart_products.append(
            {
                "product_id": pid,
                "product": p["product"],
                "category": p["category"],
                "price": price_each,
                "quantity": qty,
                "line_total": line_total,
            }
        )

    return render_template(
        "cart.html",
        products=cart_products,
        total=cart_total,
    )


@app.route("/clear_cart", methods=["POST"])
def clear_cart():
    """
    Clear current cart in session.
    """
    session["cart"] = []
    return redirect(url_for("cart_view"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """
    Checkout page:
      - GET: show order summary and shipping method.
      - POST: save order to DB, create invoice, clear cart and redirect to success page.
    """
    cart_ids = get_cart_ids()
    if not cart_ids:
        return redirect(url_for("cart_view"))

    customer_id = session.get("customer_id")
    if not customer_id:
        flash("Please log in before checkout.", "error")
        return redirect(url_for("login"))

    is_company = session.get("is_company", False)

    all_products = pm.get_all_products()
    counts = Counter(cart_ids)
    products_by_id = {p["product_id"]: p for p in all_products}

    items = []
    total = 0.00
    for pid, qty in counts.items():
        p = products_by_id.get(pid)
        if not p or qty <= 0:
            continue
        price = float(p["price"])
        line_total = price * qty
        total += line_total
        items.append(
            {
                "product_id": pid,
                "product": p["product"],
                "category": p["category"],
                "price": price,
                "quantity": qty,
                "line_total": line_total,
            }
        )

    discount_factor = 0.95 if is_company else 1.0
    total_with_discount = total * discount_factor

    om = OrderMethods()

    if request.method == "GET":
        return render_template(
            "checkout.html",
            items=items,
            total=total_with_discount,
            is_company=is_company,
        )

    # POST: save order and create invoice
    shipping_method = request.form.get("shipping_method", "standard")
    session["shipping_method"] = shipping_method

    cart = ShoppingCart(customer_id=customer_id)
    for pid, qty in counts.items():
        cart.add_product(pid, qty)

    cart.calculate_total_price(pm)

    order_id = om.save_order(cart, is_company=is_company)
    if not order_id:
        flash("An error occurred while saving the order.", "error")
        return redirect(url_for("cart_view"))

    # create invoice (only here, NOT in order_success)
    order = Order(cart, is_company=is_company)
    order.set_order_id(order_id)
    order.create_invoice()

    # clear session cart
    session["cart"] = []
    return redirect(url_for("order_success", order_id=order_id))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page:
      - GET: show empty form
      - POST: validate, save customer, handle errors with flash messages.
    """
    if request.method == "POST":
        form = request.form.to_dict()

        name = form.get("name", "").strip().title()
        email = form.get("email", "").strip().title()
        address = form.get("address") or None
        phone = form.get("phone") or None
        kind = form.get("kind", "private").lower()
        password = form.get("password", "")
        password2 = form.get("password2", "")
        birthdate = form.get("birthdate") or None
        company_number = form.get("company_number") or None

        try:
            # 1) Check if passwords match
            if password != password2:
                raise ValueError("Passwords do not match.")

            # 2) Try to save customer using CustomerMethods (with Pydantic inside)
            try:
                new_id = cm.save_customer(
                    name=name,
                    email=email,
                    address=address,
                    phone=phone,
                    kind=kind,
                    password=password,
                    birthdate=birthdate,
                    company_number=company_number,
                )
            except ValidationError as err:
                # extract field name from Pydantic error
                field = err.errors()[0].get("loc", ["?"])[0]
                field_map = {
                    "name": "Name",
                    "email": "Email",
                    "address": "Address",
                    "phone": "Phone",
                    "birthdate": "Birthdate",
                    "company_number": "Company number",
                    "password": "Password",
                    "kind": "Kind",
                }
                label = field_map.get(field, str(field).capitalize())
                # raise ValueError with short readable message
                Validator.f_short_err(err, label)

            # 3) If save_customer returned None → generic failure
            if not new_id:
                flash("Registration failed. Please try again later.", "error")
                return render_template("register.html", form=form)

            # 4) Success
            flash(
                f"Registration successful, {name}!\n"
                f"Your customer number is {new_id}.\n"
                "Please save your customer number and password.\n"
                "You can now log in.",
                "success",
            )
            return redirect(url_for("login"))

        except ValueError as e:
            # All our "nice" messages arrive here
            flash(str(e), "error")
            return render_template("register.html", form=form)

        except Exception as e:
            print("Unexpected error in /register:", e)
            flash("Unexpected error. Please try again later.", "error")
            return render_template("register.html", form=form)

    return render_template("register.html", form={})


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page:
      - GET: show form
      - POST: check email/password, set session and redirect to products.
    """
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # 1) Simple check for empty fields
        if not email or not password:
            error = "Please enter your email address and password."
        else:
            # 2) Load user from DB
            user = cm.get_customer_by_email(email)

            # 3) Validate user and password
            if not user or not check_password(user, password):
                error = "Incorrect email or password."
            else:
                # 4) Login successful → store session data
                session.clear()

                session["customer_id"] = user["customer_id"]
                session["user_email"] = user["email"]
                session["user_name"] = user["name"]
                session["customer_name"] = user["name"]
                session["customer_kind"] = user["kind"]          # 'private' or 'company'
                session["is_company"] = (user["kind"] == "company")

                flash(f"Logged in as {user['name']}.", "success")
                return redirect(url_for("product_list"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """
    Clear all user-related session keys and redirect to products page.
    """
    session.pop("user_email", None)
    session.pop("customer_id", None)
    session.pop("user_name", None)
    session.pop("customer_kind", None)
    session.pop("is_company", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("product_list"))


@app.route("/order_success/<int:order_id>")
def order_success(order_id: int):
    """
    Order success page:
      - loads order header and items from DB,
      - calculates subtotal / discount / total (based on company flag),
      - shows summary and shipping method.
    Invoice is already created during checkout, not here.
    """
    om = OrderMethods()
    try:
        # 1) Order header + basic customer data
        order_row = om.storage.fetch_one(
            """
            SELECT o.order_id,
                   o.customer_id,
                   o.order_date,
                   o.total,
                   c.name,
                   c.email,
                   c.address,
                   c.kind AS kind
            FROM orders o
            JOIN customers c ON c.customer_id = o.customer_id
            WHERE o.order_id = %s
            """,
            (order_id,),
        )

        if not order_row:
            return redirect(url_for("cart_view"))

        # 2) Order items
        items = om.storage.fetch_all(
            """
            SELECT oi.product_id,
                   p.product,
                   p.category,
                   oi.quantity,
                   oi.price
            FROM order_items oi
            JOIN product p ON p.product_id = oi.product_id
            WHERE oi.order_id = %s
            """,
            (order_id,),
        )

        # 3) Calculate subtotal and line totals
        subtotal = 0.0
        for row in items:
            line_total = float(row["price"]) * row["quantity"]
            row["line_total"] = line_total
            subtotal += line_total

        is_company = (order_row["kind"] == "company")
        total_db = float(order_row["total"])

        if is_company:
            discount_amount = subtotal - total_db
            total = total_db
        else:
            discount_amount = 0.0
            total = subtotal

        # 4) Shipping method stored in session during checkout
        shipping_method = session.get("shipping_method", "standard")

        return render_template(
            "order_success.html",
            order=order_row,
            customer=order_row,      # for template convenience (customer.name, customer.kind, ...)
            items=items,
            subtotal=subtotal,
            discount=discount_amount,
            total=total,
            is_company=is_company,
            shipping_method=shipping_method,
        )
    finally:
        om.close()


@app.route("/reviews", methods=["GET", "POST"])
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
                    "reviews_view",
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


@app.route("/my_orders")
def my_orders():
    """
    "My orders" page:
      - loads all orders for current customer,
      - calculates subtotal/discount/total for each order and global sums.
    """
    customer_id = session.get("customer_id")
    if not customer_id:
        return redirect(url_for("login"))

    om = OrderMethods()
    orders = om.get_orders_with_items_for_customer(customer_id)

    total_subtotal = 0.0
    total_discount = 0.0
    total_final = 0.0

    for order in orders:
        subtotal = sum(item["price"] * item["quantity"] for item in order["items"])
        total = order["total"]
        discount = subtotal - total

        order["subtotal"] = subtotal
        order["discount"] = discount
        order["discount_percent"] = 5 if session.get("is_company") else 0

        total_subtotal += subtotal
        total_discount += discount
        total_final += total

    return render_template(
        "orders_history.html",
        orders=orders,
        total_subtotal=total_subtotal,
        total_discount=total_discount,
        total_final=total_final,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Profile page:
      - GET: show user data
      - POST: update name, email, address, phone using Validator and CustomerMethods.
    """
    customer_id = session.get("customer_id")
    if not customer_id:
        flash("Please log in to access your profile.", "error")
        return redirect(url_for("login"))

    # load current customer from DB
    user = cm.get_customer_by_id(customer_id)
    if not user:
        flash("Customer not found.", "error")
        return redirect(url_for("product_list"))

    error = None
    success = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()

        try:
            # example validation via your Validator class
            name = Validator.validate_name(name)
            email = Validator.validate_email(email)
            address = Validator.validate_address(address)
            phone = Validator.validate_phone(phone)

            ok = cm.update_customer(
                customer_id=customer_id,
                name=name,
                email=email,
                address=address,
                phone=phone,
            )

            if not ok:
                error = "Could not update profile. Please try again."
            else:
                # update session so navbar shows new name/email
                session["user_name"] = name
                session["user_email"] = email
                success = "Profile updated successfully."

                # reload user from DB to show fresh data in the form
                user = cm.get_customer_by_id(customer_id)

        except ValueError as e:
            error = str(e)

    return render_template(
        "profile.html",
        user=user,
        error=error,
        success=success,
    )



if __name__ == "__main__":
    app.run(debug=True)
