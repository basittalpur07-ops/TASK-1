import csv
from datetime import datetime


class Order:
    products_file = "products.csv"
    log_file = "log.txt"
    discount_rate = 0  

    def __init__(self):
        self.items = []

    @staticmethod
    def log_action(func):
        """Decorator to log method execution automatically."""
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            with open(Order.log_file, "a") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executed {func.__name__}\n")
            return result
        return wrapper

    @staticmethod
    def is_valid_product_id(product_id):
        """Check if product ID exists in products.csv"""
        try:
            with open(Order.products_file, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if int(row["id"]) == product_id:
                        return True
        except FileNotFoundError:
            with open(Order.log_file, "a") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: products.csv not found\n")
        
        with open(Order.log_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Invalid product ID attempt: {product_id}\n")
        return False

    
    @log_action
    def add_item_by_id(self, product_id, quantity):
        """Add a product to the order by product ID"""
        if not Order.is_valid_product_id(product_id):
            return

        with open(Order.products_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["id"]) == product_id:
                    name = row["name"]
                    price = float(row["price"])
                    total_price = price * quantity
                    self.items.append((name, quantity, total_price))
                    with open(Order.log_file, "a") as f:
                        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Added item: {name} (x{quantity}) - Total: {total_price}\n")
                    break

    @log_action
    def calculate_total(self):
        """Calculate total price with discount if applied"""
        total = sum(item[2] for item in self.items)
        if Order.discount_rate > 0:
            discount_amount = total * (Order.discount_rate / 100)
            total -= discount_amount
        with open(Order.log_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Calculated total with discount: {total}\n")
        return total

    
    @classmethod
    def set_discount(cls, discount_rate):
        """Set a global discount for all orders"""
        cls.discount_rate = discount_rate
        with open(Order.log_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Discount set to {discount_rate}%\n")


if __name__ == "__main__":
    order = Order()

    order.add_item_by_id(1, 2)   
    order.add_item_by_id(4, 3) 

    order.add_item_by_id(99, 1)

    Order.set_discount(10)

    final_total = order.calculate_total()

    print(f"Final total after discount: {final_total}")
    print("Check log.txt for detailed actions.")

