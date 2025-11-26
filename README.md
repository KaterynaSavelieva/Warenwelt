Warenwelt/
│
├── app.py                 # тільки створення Flask app + реєстрація blueprint'ів
│
├── controllers/           # C = Controllers
│   ├── __init__.py
│   ├── products_controller.py
│   ├── customers_controller.py
│   ├── orders_controller.py
│   └── reviews_controller.py
│
├── models/                # M = Models (те, що зараз у customers/, products/, orders/, reviews/)
│   ├── __init__.py
│   ├── customers/
│   │   ├── customer.py
│   │   ├── private_customer.py
│   │   ├── company_customer.py
│   │   └── customer_methods.py
│   ├── products/
│   │   ├── product.py
│   │   └── product_methods.py
│   ├── orders/
│   │   ├── order.py
│   │   ├── order_methods.py
│   │   └── shopping_cart.py
│   └── reviews/
│       ├── review.py
│       └── review_methods.py
│
├── views/                 # V = Views (HTML)
│   └── templates/
│       ├── base.html
│       ├── products.html
│       ├── cart.html
│       ├── profile.html
│       └── reviews.html
│
├── static/                # CSS / JS / images (можна лишити як є)
│
├── database/              # колишній connection/
│   ├── __init__.py
│   ├── db.py
│   └── storage.py
│
├── utils/
│   ├── validator.py
│   └── input_helpers.py
│
└── cli/                   # консольні меню (можна не чіпати)
    ├── cli_main.py
    ├── product_management.py
    ├── customers_management.py
    └── orders_main.py
