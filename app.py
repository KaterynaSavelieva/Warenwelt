from flask import Flask, render_template
from products.product_methods import ProductMethods

app = Flask(__name__)
app.secret_key = "change_me_to_a_random_secret_key"

product_methods = ProductMethods()


@app.route("/")
def product_list():

    products = product_methods.get_all_products()
    return render_template("products.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)
