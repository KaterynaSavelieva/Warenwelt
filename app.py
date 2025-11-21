from flask import Flask, render_template, request, redirect, url_for, session, flash
from products.product_methods import ProductMethods    # доступ до БД
from collections import Counter
from decimal import Decimal
from orders.shopping_cart import ShoppingCart
from orders.order import Order
from orders.order_methods import OrderMethods
from customers.customer_methods import CustomerMethods
from reviews.review_methods import ReviewMethods
from connection.storage import Storage
from customers.validator import Validator



app = Flask(__name__)
app.secret_key = "change_me_to_a_random_secret_key"

def eur(value):
    """Форматує число як 0 000,00 для відображення в EUR."""
    if value is None:
        return "0,00"
    try:
        # підтримка Decimal, float, int
        if isinstance(value, Decimal):
            value = float(value)
        else:
            value = float(value)
    except (TypeError, ValueError):
        return "0,00"

    s = f"{value:,.2f}"        # напр. '16,199.82'
    s = s.replace(",", " ")    # '16 199.82'
    s = s.replace(".", ",")    # '16 199,82'
    return s

app.jinja_env.filters["eur"] = eur

pm = ProductMethods()                    # один екземпляр для всіх запитів
cm = CustomerMethods()
rm = ReviewMethods()

# ---------- helper-функції для кошика в сесії ----------

def get_cart_ids() -> list[int]:
    """Читає з сесії список cart. Якщо там нічого немає — повертає порожній список."""
    return session.get("cart", [])

def add_to_cart(product_id: int) -> None:
    """Бере наявний список, додає новий product_id і зберігає назад у session['cart']."""
    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart

def calculate_cart_total(products, counts: Counter) -> float:
    #Рахує загальну суму кошика на основі products + Counter(product_id).
    total = 0.0
    for p in products:
        pid = p["product_id"]
        qty = counts.get(pid, 0)
        if qty > 0:
            price_each = float(p["price"])
            total += qty * price_each
    return total

def check_password (user_row: dict, plain_password: str) -> bool: #password check: compares plain text from form with the value from database.
    if not user_row:
        return False
    db_password = user_row.get("password")
    if db_password is None:
        return False
    return db_password == plain_password

# ---------- маршрути ----------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def product_list():
    view = request.args.get("view", "table")
    if view not in ("table", "cards"):
        view = "table"

    # ---- параметри фільтра та сортування ----
    search    = request.args.get("search", "").strip()
    category  = request.args.get("category", "").strip()
    brand     = request.args.get("brand", "").strip()
    author    = request.args.get("author", "").strip()
    size      = request.args.get("size", "").strip()
    sort      = request.args.get("sort", "id")
    direction = request.args.get("dir", "asc")

    # ---- Всі продукти (для фільтрів + суми кошика) ----
    all_products = pm.get_all_products()          # без фільтрів!

    cart_ids = get_cart_ids()
    counts = Counter(cart_ids)
    cart_total = calculate_cart_total(all_products, counts)

    # списки для випадаючих меню
    categories = sorted({p["category"] for p in all_products})
    brands     = sorted({p["brand"]   for p in all_products if p.get("brand")})
    authors    = sorted({p["author"]  for p in all_products if p.get("author")})
    sizes = sorted({p["size"] for p in all_products if p.get("size")})

    # ---- Список товарів з фільтрами з БД ----
    products = pm.get_products_filtered(
        search=search,
        category=category,
        brand=brand,
        author=author,
        size=size,
    )

    # ---- Сортування в Python (додаємо rating) ----
    def total_for(p):
        return counts.get(p["product_id"], 0) * float(p["price"])

    key_map = {
        "id":       lambda p: p["product_id"],
        "name":     lambda p: p["product"],
        "category": lambda p: p["category"],
        "price":    lambda p: float(p["price"]),
        "total":    total_for,
        "rating":   lambda p: float(p["avg_rating"] or 0.0),   # НОВЕ
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
        categories=categories,   # для select
        brands=brands,
        authors=authors,
        sizes=sizes,
    )


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart_route(product_id: int):
    """Обробник кліку на кнопку 'In den Warenkorb'."""
    add_to_cart(product_id)                           # додаємо товар у кошик

    # зберігаємо поточний режим відображення (table/cards), якщо він був у query params
    view = request.args.get("view", "table")
    if view not in ("table", "cards"):
        view = "table"

    # повертаємося на головну сторінку
    return redirect(url_for("product_list", view=view))

@app.route("/set_cart_quantity/<int:product_id>", methods=["POST"])
def set_cart_quantity(product_id: int):
    cart = get_cart_ids()
    try:
        qty = int(request.form.get("qty", "0"))
    except ValueError:
        qty = 0

    if qty < 0:
        qty = 0

    # видаляємо всі старі входження
    cart = [pid for pid in cart if pid != product_id]
    # додаємо стільки разів, скільки треба
    cart.extend([product_id] * qty)
    session["cart"] = cart

    # повертаємось туди ж, де були (з якорем)
    return_url = request.form.get("return_url")
    if return_url:
        return redirect(return_url)

    return redirect(request.referrer or url_for("product_list"))

@app.route("/cart")
def cart_view():
    """Сторінка кошика з кількістю, сумою по рядку та загальною сумою."""
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

        cart_products.append({
            "product_id": pid,
            "product": p["product"],
            "category": p["category"],
            "price": price_each,
            "quantity": qty,
            "line_total": line_total,
        })

    return render_template(
        "cart.html",
        products=cart_products,
        total=cart_total,
    )

@app.route("/clear_cart", methods=["POST"]) #маршрут для очищення кошика
def clear_cart():
    session["cart"] = []
    return redirect(url_for("cart_view"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
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
        items.append({
            "product_id": pid,
            "product": p["product"],
            "category": p["category"],
            "price": price,
            "quantity": qty,
            "line_total": line_total,
        })

    discount_factor = 0.95 if is_company else 1.0
    total_with_discount = total * discount_factor

    # ВАЖЛИВО: створюємо тут
    om = OrderMethods()

    if request.method == "GET":
        return render_template(
            "checkout.html",
            items=items,
            total=total_with_discount,
            is_company=is_company,
        )

    # POST
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

    # створюємо інвойс
    order = Order(cart, is_company=is_company)
    order.set_order_id(order_id)
    order.create_invoice()

    session["cart"] = []
    return redirect(url_for("order_success", order_id=order_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form.to_dict()

        name = form.get("name", "").strip()
        email = form.get("email", "").strip()
        address = form.get("address") or None
        phone = form.get("phone") or None
        kind = form.get("kind", "private").lower()
        password = form.get("password", "")
        password2 = form.get("password2", "")
        birthdate = form.get("birthdate") or None
        company_number = form.get("company_number") or None

        try:
            if password != password2:
                raise ValueError("Passwords do not match.")

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

            if not new_id:
                flash("Registration failed. Please try again later.", "error")
                return render_template("register.html", form=form)

            flash(
                f"Registration successful, {name}!\n"
                f"Your customer number is {new_id}. \n"
                "Please save your customer number and password. \n"
                "You can now log in.",
                "success"
            )
            return redirect(url_for("login"))

        except ValueError as e:
            flash(str(e), "error")
            return render_template("register.html", form=form)

        except Exception as e:
            print("Unexpected error in /register:", e)
            flash("Unexpected error. Please try again later.", "error")
            return render_template("register.html", form=form)

    return render_template("register.html", form={})

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # 1) Simple check for empty fields
        #   проста перевірка, що поля не порожні
        if not email or not password:
            error = "Please enter your email address and password.."
        else:
            # 2) Load user from database
            #  шукаємо користувача в БД
            user = cm.get_customer_by_email(email)

            # 3)  Validate user and password
            #  якщо немає юзера або пароль не збігається → помилка
            if not user or not check_password(user, password):
                error = "Incorrect email or password."

            else:
                # 4) Login successful → store user session
                # логін успішний → зберігаємо дані в сесії
                session.clear() # optional: очистити старі дані

                session["customer_id"]= user ["customer_id"]
                session["user_email"] = user["email"]
                session["user_name"] = user["name"]
                session["customer_name"] = user["name"]
                session["customer_kind"] = user["kind"]     # 'private' or 'company'
                session["is_company"] = (user["kind"]=="company") #is_company – True для kind == 'company', інакше False.

                flash("Logged in as {}.".format(user["name"]), "success")
                return redirect(url_for("product_list"))

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user_email", None)
    session.pop("customer_id", None)
    session.pop("user_name", None)
    session.pop("customer_kind", None)
    session.pop("is_company", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("product_list"))

@app.route("/order_success/<int:order_id>")
def order_success(order_id: int):
    om = OrderMethods()          # новий інстанс на КОЖЕН запит
    try:
        # 1) Заголовок замовлення + дані клієнта
        order_row = om.storage.fetch_one(
            """
            SELECT b.order_id,
                   b.customer_id,
                   b.order_date,
                   b.total,
                   c.name,
                   c.email,
                   c.address,
                   c.kind AS customer_kind
            FROM orders b
            JOIN customers c ON c.customer_id = b.customer_id
            WHERE b.order_id = %s
            """,
            (order_id,),
        )

        if not order_row:
            return redirect(url_for("cart_view"))

        # 2) Рядки замовлення
        items = om.storage.fetch_all(
            """
            SELECT d.product_id,
                   p.product,
                   p.category,
                   d.quantity,
                   d.price
            FROM order_items d
            JOIN product p ON p.product_id = d.product_id
            WHERE d.order_id = %s
            """,
            (order_id,),
        )

        # ... твій код підрахунку subtotal / discount / total ...
        subtotal = 0.0
        for row in items:
            line_total = float(row["price"]) * row["quantity"]
            row["line_total"] = line_total
            subtotal += line_total

        is_company = (order_row["customer_kind"] == "company")
        total_db = float(order_row["total"])

        if is_company:
            discount_amount = subtotal - total_db
            total = total_db
        else:
            discount_amount = 0.0
            total = subtotal

        # ShoppingCart + invoice як було
        cart = ShoppingCart(customer_id=order_row["customer_id"])
        for row in items:
            cart.add_product(row["product_id"], row["quantity"])
        cart.total_sum = subtotal

        order_obj = Order(cart, is_company=is_company)
        order_obj.set_order_id(order_id)
        invoice_path = order_obj.create_invoice()

        shipping_method = session.get("shipping_method", "standard")

        return render_template(
            "order_success.html",
            order=order_row,
            items=items,
            subtotal=subtotal,
            discount=discount_amount,
            total=total,
            is_company=is_company,
            invoice_path=invoice_path,
            shipping_method=shipping_method,
        )
    finally:
        om.close()   # закриваємо з’єднання

@app.route("/reviews", methods=["GET", "POST"])
def reviews_view():
    storage = Storage()
    storage.connect()

    customer_id = session.get("customer_id")
    error = None

    # -------- параметри фільтра / сортування з URL --------
    search = (request.args.get("search") or "").strip()
    category_filter = request.args.get("category", "")
    rating_filter = request.args.get("rating", "")
    sort = request.args.get("sort", "date")
    direction = request.args.get("dir", "desc")

    # дозволені поля сортування
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

    # -------- якщо POST: додаємо новий відгук --------
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

        # перевіряємо, чи клієнт дійсно купував цей товар
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
            # після успішного запису – повертаємось на GET з тими ж фільтрами
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

    # -------- 1) всі відгуки з фільтрацією/сортуванням --------
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

    # -------- 2) продукти, які поточний клієнт може оцінити --------
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

    # -------- 3) список категорій для випадаючого списку --------
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
        # параметри для шаблону
        search=search,
        category_filter=category_filter,
        rating_filter=rating_filter,
        sort=sort,
        direction=direction,
    )


@app.route("/my_orders")
def my_orders():
    customer_id = session.get("customer_id")
    if not customer_id:
        return redirect(url_for("login"))

    om = OrderMethods()
    orders = om.get_orders_with_items_for_customer(customer_id)

    total_subtotal = 0
    total_discount = 0
    total_final = 0

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
    customer_id = session.get("customer_id")
    if not customer_id:
        flash("Please log in to access your profile.", "error")
        return redirect(url_for("login"))

    # завантажуємо поточного користувача
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

        # якщо хочеш – підключи свій Validator
        try:
            # приклад – адаптуй під свої методи
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
                # оновлюємо дані в session, щоб у шапці показувалось нове ім’я/емейл
                session["user_name"] = name
                session["user_email"] = email
                success = "Profile updated successfully."

                # перезавантажимо user, щоб у формі були свіжі дані
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