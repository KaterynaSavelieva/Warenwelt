from methods.product_methods import ProductMethods

#pm = ProductMethods()

if __name__ == "__main__":
    products = ProductMethods ()
    products.get_all_products()
    products.get_product(12)
    products.close()
