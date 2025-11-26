from flask import session
from collections import Counter
from decimal import Decimal

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

