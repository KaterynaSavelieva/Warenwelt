from flask import Flask, render_template, request, redirect, url_for, session, flash
from products.product_methods import ProductMethods    # доступ до БД
from collections import Counter
from decimal import Decimal
from orders.shopping_cart import ShoppingCart
from orders.order import Order
from orders.order_methods import OrderMethods
from customers.customer_methods import CustomerMethods

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

product_methods = ProductMethods()                    # один екземпляр для всіх запитів
order_methods = OrderMethods()
customer_methods = CustomerMethods()

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
    """Рахує загальну суму кошика на основі products + Counter(product_id)."""
    total = 0.0
    for p in products:
        pid = p["product_id"]
        qty = counts.get(pid, 0)
        if qty > 0:
            price_each = float(p["price"])
            total += qty * price_each
    return total

# ---------- маршрути ----------

@app.route("/")
def product_list():
    view = request.args.get("view", "table")
    if view not in ("table", "cards"):
        view = "table"

    # ---- параметри фільтра та сортування ----
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "id")
    direction = request.args.get("dir", "asc")

    products = product_methods.get_all_products()

    # ---- кошик ----
    cart_ids = get_cart_ids()
    counts = Counter(cart_ids)

    def total_for(p):
        return counts.get(p["product_id"], 0) * float(p["price"])

    # ---- фільтрація ----
    filtered = products

    if category:
        filtered = [p for p in filtered if p["category"] == category]

    if search:
        term = search.lower()
        filtered = [
            p for p in filtered
            if term in p["product"].lower()
        ]

    # ---- сортування по будь-якому полю ----
    key_map = {
        "id":       lambda p: p["product_id"],
        "name":     lambda p: p["product"],
        "category": lambda p: p["category"],
        "price":    lambda p: float(p["price"]),
        "total":    total_for,
    }
    key_func = key_map.get(sort, key_map["id"])
    reverse = (direction == "desc")
    filtered = sorted(filtered, key=key_func, reverse=reverse)

    # загальна сума всього кошика (по всіх товарах, не тільки відфільтрованих)
    cart_total = calculate_cart_total(products, counts)

    return render_template(
        "products.html",
        products=filtered,
        view=view,
        counts=counts,
        cart_total=cart_total,
        search=search,
        category=category,
        sort=sort,
        direction=direction,
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

    all_products = product_methods.get_all_products()

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

    # ---- хто робить замовлення? ----
    customer_id = session.get("customer_id", 1)        # тимчасово 1
    is_company = session.get("is_company", False)      # True/False з login

    # ---- всі продукти з БД + кількості з сесії ----
    all_products = product_methods.get_all_products()
    counts = Counter(cart_ids)

    products_by_id = {p["product_id"]: p for p in all_products}

    items = []
    total = 0.0

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

    # застосовуємо знижку тільки логічно (у БД вже робиться в OrderMethods)
    discount_factor = 0.95 if is_company else 1.0
    total_with_discount = total * discount_factor

    # ---- GET: просто показати підсумкову таблицю ----
    if request.method == "GET":
        return render_template(
            "checkout.html",
            items=items,
            total=total_with_discount,   # вже зі знижкою
            is_company=is_company,       # щоб у шаблоні показати "5% Rabatt"
        )

    # ---- POST: користувач натиснув "Bestellung abschließen" ----

    # 1) будуємо ShoppingCart з того, що лежить у сесії
    cart = ShoppingCart(customer_id=customer_id)

    for pid, qty in counts.items():
        cart.add_product(pid, qty)

    # порахувати total_sum всередині кошика (для Order)
    cart.calculate_total_price(product_methods)

    # 2) зберігаємо замовлення в БД за допомогою ТВОГО OrderMethods
    order_id = order_methods.save_order(cart, is_company=is_company)
    if not order_id:
        flash("Beim Speichern der Bestellung ist ein Fehler aufgetreten.", "error")
        return redirect(url_for("cart_view"))

    # 3) створюємо обʼєкт Order (твій клас) і генеруємо інвойс
    order = Order(cart, is_company=is_company)
    order.set_order_id(order_id)
    order.create_invoice()

    # 4) чистимо кошик у сесії й показуємо success
    session["cart"] = []
    flash("Ihre Bestellung wurde erfolgreich abgeschlossen.", "success")
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

            new_id = customer_methods.save_customer(
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
                f"Registration successful! Your customer number is {new_id}. "
                f"Please write down your number and password.",
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

        # TODO: тут перевірка у БД
        # user = customer_methods.find_by_email(email)
        # if not user or not check_password(user, password): ...

        if not email or not password:
            error = "Bitte geben Sie Email und Passwort ein."
        else:
            # Поки що – фейк: вважаємо, що логін завжди успішний
            session["user_email"] = email
            flash("Erfolgreich eingeloggt.", "success")
            return redirect(url_for("product_list"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    flash("Sie wurden ausgeloggt.", "success")
    return redirect(url_for("product_list"))


@app.route("/order_success/<int:order_id>")
def order_success(order_id: int):
    om = OrderMethods()

    # 1) Заголовок замовлення
    order_row = om.storage.fetch_one(
        """
        SELECT b.order_id,
               b.customer_id,
               b.order_date,
               b.total,
               c.kind AS customer_kind
        FROM bestellung b
        JOIN customers c ON c.customer_id = b.customer_id
        WHERE b.order_id = %s
        """,
        (order_id,),
    )

    if not order_row:
        om.close()
        return redirect(url_for("cart_view"))

    # 2) Рядки замовлення
    items = om.storage.fetch_all(
        """
        SELECT d.product_id,
               p.product,
               p.category,
               d.quantity,
               d.price
        FROM bestellung_details d
        JOIN product p ON p.product_id = d.product_id
        WHERE d.order_id = %s
        """,
        (order_id,),
    )

    # 2.1) Рахуємо проміжну суму (без знижки) і суму по рядку
    subtotal = 0.0
    for row in items:
        line_total = float(row["price"]) * row["quantity"]
        row["line_total"] = line_total   # щоб у шаблоні показати Gesamt
        subtotal += line_total

    is_company = (order_row["customer_kind"] == "company")

    # total із БД (там уже знижка 5 % для company)
    total_db = float(order_row["total"])

    if is_company:
        discount_amount = subtotal - total_db   # скільки саме знижки
        total = total_db                        # фінальна сума
    else:
        discount_amount = 0.0
        total = subtotal

    # 3) Тимчасовий ShoppingCart для знімка (для TXT-інвойсу)
    cart = ShoppingCart(customer_id=order_row["customer_id"])
    for row in items:
        cart.add_product(row["product_id"], row["quantity"])

    # ВАЖЛИВО: тут кладемо **subtotal**, а не total_db
    cart.total_sum = subtotal

    # 4) Створюємо Order зі знімка кошика
    order_obj = Order(cart, is_company=is_company)
    order_obj.set_order_id(order_id)

    # 5) Генеруємо TXT-інвойс з деталями
    invoice_path = order_obj.create_invoice()

    om.close()

    return render_template(
        "order_success.html",
        order=order_row,
        items=items,
        subtotal=subtotal,
        discount=discount_amount,
        total=total,
        is_company=is_company,
        invoice_path=invoice_path,
    )


if __name__ == "__main__":
    app.run(debug=True)
