from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from products.product_methods import ProductMethods
from utils.cart_helpers import get_cart_ids, add_to_cart, calculate_cart_total, check_password, eur
from collections import Counter

from orders.shopping_cart import ShoppingCart
from orders.order import Order
from orders.order_methods import OrderMethods
from customers.customer_methods import CustomerMethods
from reviews.review_methods import ReviewMethods

orders_bp = Blueprint("orders", __name__)

pm = ProductMethods()
cm = CustomerMethods()
rm = ReviewMethods()


@orders_bp.route("/my_orders")
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

@orders_bp.route("/order_success/<int:order_id>")
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

@orders_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart_route(product_id: int):
    add_to_cart(product_id)

    return_url = request.form.get("return_url")
    if return_url:
        return redirect(return_url)

    view = request.args.get("cli", "table")
    if view not in ("table", "cards"):
        view = "table"

    return redirect(url_for("products.product_list", view=view))

@orders_bp.route("/set_cart_quantity/<int:product_id>", methods=["POST"])
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

@orders_bp.route("/cart")
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

@orders_bp.route("/clear_cart", methods=["POST"])
def clear_cart():
    """
    Clear current cart in session.
    """
    session["cart"] = []
    return redirect(url_for("orders.cart_view"))

@orders_bp.route("/checkout", methods=["GET", "POST"])
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
        return redirect(url_for("customers.login"))

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
    return redirect(url_for("orders.order_success", order_id=order_id))
