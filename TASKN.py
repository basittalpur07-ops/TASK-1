import csv
from datetime import datetime
from functools import wraps


class Order:
    products_file = "products.csv"
    log_file = "log.txt"
    discount_rate = 0.0

    def __init__(self):
        self.items = []

    @classmethod
    def log(cls, message):
        with open(cls.log_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    @classmethod
    def log_action(cls, func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            cls.log(f"Executed {func.__name__}")
            return result
        return wrapper

    @staticmethod
    def is_valid_product_id(product_id):
        try:
            with open(Order.products_file, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row["id"]) == product_id:
                        return True
        except FileNotFoundError:
            Order.log("Products file not found!")
        Order.log(f"Invalid product ID attempt: {product_id}")
        return False

    @log_action
    def add_item_by_id(self, product_id, quantity):
        if not Order.is_valid_product_id(product_id):
            return
        with open(Order.products_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["id"]) == product_id:
                    name = row["name"]
                    price = float(row["price"])
                    total = price * quantity
                    self.items.append((name, price, quantity, total))
                    Order.log(f"Added item: {name} (x{quantity}) - Total: {total}")
                    break

    @log_action
    def calculate_total(self):
        subtotal = sum(item[3] for item in self.items)
        discount_amount = subtotal * Order.discount_rate
        final_total = subtotal - discount_amount
        Order.log(f"Calculated total with discount: {final_total:.2f}")
        return final_total

    @classmethod
    @log_action
    def set_discount(cls, discount_rate):
        cls.discount_rate = discount_rate
        cls.log(f"Discount set to {discount_rate * 100:.0f}%")


if __name__ == "__main__":
    order = Order()
    order.add_item_by_id(1, 2)
    order.add_item_by_id(4, 3)
    order.add_item_by_id(99, 1)
    Order.set_discount(0.10)
    total = order.calculate_total()
    print("Final Total:", total)
    print("Check log.txt for all actions!")
