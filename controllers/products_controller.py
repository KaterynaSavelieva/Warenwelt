from flask import Blueprint, render_template, request
from models.products.product_methods import ProductMethods
from utils.cart_helpers import get_cart_ids, calculate_cart_total
from collections import Counter

products_bp = Blueprint("products", __name__)
pm = ProductMethods()

@products_bp.route("/products")
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

    if category == "electronics":
        author = ""
        size = ""
    elif category == "books":
        brand = ""
        size = ""
    elif category == "clothing":
        brand = ""
        author = ""

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
