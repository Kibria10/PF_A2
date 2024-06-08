class Customer:
    def __init__(self, ID, name, reward):
        pass

    def get_reward(self):
        pass

    def get_discount(self):
        pass

    def update_reward(self, amount):
        pass

    def display_info(self):
        pass


class BasicCustomer(Customer):
    def __init__(self, ID, name, reward):
        pass

    def get_reward(self, total_cost):
        pass

    def update_reward(self, value):
        pass

    def display_info(self):
        pass

    @classmethod
    def set_reward_rate(cls, new_rate):
        pass


class VIPCustomer(Customer):
    def __init__(self, ID, name, reward, discount_rate):
        pass

    def get_discount(self, total_cost):
        pass

    def get_reward(self, total_cost):
        pass

    def update_reward(self, value):
        pass

    def display_hint(self):
        pass

    @classmethod
    def set_reward_rate(cls, new_rate):
        pass

    def set_discount_rate(self, new_discount_rate):
        pass


class Product:
    def __init__(self, ID, name, price):
        pass

    def display_info(self):
        pass


class Order:
    def __init__(self, customer, product, quantity):
        pass

    def compute_cost(self):
        pass


class Records:
    def __init__(self):
        pass

    def read_customers(self, filename):
        pass

    def read_products(self, filename):
        pass

    def find_customer(self, identifier):
        pass

    def find_product(self, identifier):
        pass

    def list_customers(self):
        pass

    def list_products(self):
        pass


class Operations:
    def __init__(self, customer_file, product_file):
        pass

    def load_data(self, customer_file, product_file):
        pass

    def display_menu(self):
        pass

    def handle_choice(self, choice):
        pass

    def make_purchase(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    operations = Operations('./customers.txt', './products.txt')
    operations.run()
