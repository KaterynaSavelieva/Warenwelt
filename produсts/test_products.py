from product_methods import ProductMethods

pm = ProductMethods()

# 1) electronics
pm.save_product(
    product_new="Laptop HP EliteBook PRO", price=1899.99, weight=2.3,
    category="electronics", brand="HP", warranty_years=2
)

# 2) clothing
pm.save_product(
    product_new="T-Shirt Cotton Gelb", price=19.9, weight=0.25,
    category="clothing", size="M"
)

# 3) books
pm.save_product(
    product_new="Der kleine Prinz 2025", price=12.5, weight=0.4,
    category="books", author="Antoine de Saint-Exupéry", page_count=96
)

# 1️⃣ Update product name + price
pm.update_product(3, name="New Laptop Pro", price=1999.99)

# 2️⃣ Delete product by ID#
pm.delete_product(9)

# 3️⃣ Перевірка після оновлення / видалення
#pm.get_all_products()

pm.get_all_products()
pm.close()
