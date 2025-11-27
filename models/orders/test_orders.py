from products.product_methods import ProductMethods
from orders.shopping_cart import ShoppingCart
from orders.order_methods import OrderMethods
from orders.order import Order

def main():
    products = ProductMethods()
    cart = ShoppingCart(customer_id=4)  # company

    try:
        #  Наповнюємо кошик
        cart.add_product(2, 2)
        cart.add_product(3, 3)

        # Рахуємо суму (оновлює cart.total_sum всередині)
        total = cart.calculate_total_price(products)
        print(f"Cart total (before discount): {total:.2f} EUR")

        # робимо "знімок" кошика ДО очищення
        order = Order(cart, is_company=True)   # тут зчитаються products і total

        # Зберігаємо в БД
        orders = OrderMethods()
        order_id = orders.save_order(cart, is_company=True)  # може очищати кошик

        if order_id:
            print(f"Order saved with ID: {order_id}")
            order.set_order_id(order_id)                     # додали ID у знімок
            invoice_path = order.create_invoice()            # генеруємо інвойс з даних знімка
            print(f"Invoice created: {invoice_path}")
        else:
            print("Order was not saved.")

    finally:
        try: orders.close()
        except Exception: pass
        try: products.close()
        except Exception: pass

if __name__ == "__main__":
    main()
