from flask import Flask, render_template

from controllers.products_controller import products_bp
from controllers.customers_controller import customers_bp
from controllers.reviews_controller import reviews_bp
from controllers.orders_controller import orders_bp

from utils.cart_helpers import eur

app = Flask(__name__, template_folder="views/templates", static_folder="static")

app.secret_key = "change_me_to_a_random_secret_key"

app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(orders_bp)

app.jinja_env.filters["eur"] = eur

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
