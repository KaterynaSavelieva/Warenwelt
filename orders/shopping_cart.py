from products.product_methods import ProductMethods

class ShoppingCart:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id # save the customer id
        self.products = []  # create an empty list to store products (as tuples),
        # each tuple looks like (product_id, quantity)
        self.total_sum = 0.0 # total price of all products in the cart


    def add_product(self, product_id: int, quantity: int = 1):
        # quantity = 1 is a default parameter value
        # if the user doesn’t give a quantity, it will automatically be 1
        self.products.append((product_id, quantity)) # add a new product (as a tuple) to the product list
        print(f"Product {product_id} added (x{quantity}).")
    # cart.add_product(5)       → quantity = 1 automatically
    # cart.add_product(5, 3)    → quantity = 3 (because it was given explicitly)

    def remove_product(self, product_id: int):
        new_list = [] # create a new empty list

        for p in self.products: # go through all items in the cart
            # p is a tuple, for example (3, 2)
            # p[0] = product_id
            # p[1] = quantity

            if p[0] != product_id: # if ID doesn’t match, keep this item
                new_list.append(p)
            else: # if it matches — skip (basically “remove”)
                print(f"Product {product_id} will be removed...")

        self.products = new_list # replace the old list of products with the new one
        print(f"Product {product_id} removed.") # final message

    def clear_cart(self):
        self.products.clear()  # remove all products from the shopping cart
        self.total_sum = 0.0 # reset the total price to zero
        print("Shopping cart has been cleared.") # show a message to confirm that the cart is empty

    def calculate_total_price(self, product_methods: ProductMethods):
        total = 0 # start total sum at 0

        for product_id, quantity in self.products: # go through each product in the cart
            product = product_methods.get_product(product_id) # get full product info from the database

            if product:  # if the product exists, add its price * quantity to the total
                total += product["price"] * quantity

        self.total_sum = float(round(total, 2))  # round the total to 2 decimal places and save it
        return self.total_sum # return the total sum