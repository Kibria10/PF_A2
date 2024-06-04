# Define the base Customer class
class Customer:
    def __init__(self, ID, name, reward):
        self.ID = ID
        self.name = name
        self.reward = reward

    # Placeholder methods for subclasses to implement specific behavior
    def get_reward(self):
        pass

    def get_discount(self):
        pass

    def update_reward(self, amount):
        pass

    def display_info(self):
        pass


# Define the BasicCustomer class inheriting from Customer
class BasicCustomer(Customer):
    reward_rate = 100  # static variable shared by all BasicCustomer instances

    def __init__(self, ID, name, reward):
        super().__init__(ID, name, reward)

    # Calculate reward based on the total cost of purchase
    def get_reward(self, total_cost):
        return round(total_cost * (BasicCustomer.reward_rate / 100))

    # Update the reward points by a given value
    def update_reward(self, value):
        self.reward += value

    # Display information specific to basic customers
    def display_info(self):
        print(
            f"ID: {self.ID}, Name: {self.name}, Reward Points: {self.reward}, Reward Rate: {BasicCustomer.reward_rate}%")

    # Class method to change the reward rate for all basic customers
    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate


# Subclass for VIP customers with both reward and discount rates
class VIPCustomer(Customer):
    reward_rate = 100  # static variable shared by all VIPCustomer instances

    def __init__(self, ID, name, reward, discount_rate=8):
        super().__init__(ID, name, reward)
        self.discount_rate = discount_rate  # Unique discount rate for VIP customers

    # Calculate discount based on the total cost
    def get_discount(self, total_cost):
        return total_cost * (self.discount_rate / 100)

    # Calculate reward, considering the discount applied
    def get_reward(self, total_cost):
        return round((total_cost - self.get_discount(total_cost)) * (VIPCustomer.reward_rate / 100))

    # Update the customer's reward points
    def update_reward(self, value):
        self.reward += value

    # Display information specific to VIP customers
    def display_info(self):
        print(
            f"ID: {self.ID}, Name: {self.name}, Reward Points: {self.reward}, Reward Rate: {VIPCustomer.reward_rate}%, Discount Rate: {self.discount_rate}%")

    # Class method to change the reward rate for all VIP customers
    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate

    # Method to change the discount rate for individual VIP customers
    def set_discount_rate(self, new_discount_rate):
        self.discount_rate = new_discount_rate


# Product class to manage product attributes
class Product:
    def __init__(self, ID, name, price, requires_prescription):
        self.ID = ID
        self.name = name
        self.price = price
        self.requires_prescription = True if requires_prescription == 'y' else False

    def display_info(self):
        prescription_status = "requires prescription" if self.requires_prescription else "no prescription required"
        print(f"ID: {self.ID}, Name: {self.name}, Price: {self.price} AUD, Prescription: {prescription_status}")


# Order class to handle transactions
class Order:
    def __init__(self, customer, product, quantity):
        self.customer = customer
        self.product = product
        self.quantity = quantity

    # Compute the cost of the order, considering discounts and calculating rewards
    def compute_cost(self):
        original_cost = self.product.price * self.quantity  # Calculate the original cost without discount
        if isinstance(self.customer, VIPCustomer):
            discount = self.customer.get_discount(original_cost)  # Calculate discount if customer is VIP
            total_cost = original_cost - discount
        else:
            discount = 0
            total_cost = original_cost
        reward = self.customer.get_reward(total_cost)  # Calculate reward points earned from the transaction
        return original_cost, discount, total_cost, reward


# Records Class to manage data operations
class Records:
    def __init__(self):
        self.customers = []
        self.products = []
        self.bundles = []


    # Read customer data from a file and populate the customers list
    def read_customers(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    # Differentiate between Basic and VIP customers based on ID prefix
                    if parts[0][0] == 'B':  # BasicCustomer
                        if len(parts) == 4:
                            customer = BasicCustomer(parts[0], parts[1], int(parts[3]))
                            self.customers.append(customer)
                    elif parts[0][0] == 'V':  # VIPCustomer
                        if len(parts) == 5:
                            customer = VIPCustomer(parts[0], parts[1], int(parts[4]), float(parts[3]))
                            self.customers.append(customer)
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Read product data from a file and populate the products list
    def read_products(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if parts[0][0] == 'B':  # Bundle identifier
                        bundle_id, bundle_name, *product_ids = parts
                        total_price = self.compute_bundle_price(product_ids)
                        bundle_requires_prescription = self.bundle_prescription_requirement(product_ids)
                        self.bundles.append(Bundle(bundle_id, bundle_name, product_ids, total_price, bundle_requires_prescription))
                    else:
                        product_id = parts[0].strip()
                        product_name = parts[1].strip()
                        price = float(parts[2].strip())
                        requires_prescription = parts[3].strip()
                        self.products.append(Product(product_id, product_name, price, requires_prescription))
                # print(len(self.products))
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred while reading product data: {e}")

    # Search for a customer by ID or name, returning the customer object if found
    def find_customer(self, identifier):
        identifier = identifier.lower().strip()  # Trim whitespace and convert to lowercase
        for customer in self.customers:
            if customer.name.lower().strip() == identifier:
                print("Hello " + customer.name)
                return customer
        return None

    def find_product_by_id(self, product_id):
        # Search in single products
        for product in self.products:
            if product.ID == product_id.strip().lstrip():
                return product
        return None

    # Search for a product by ID or name, returning the product object if found
    def find_product(self, identifier):
        identifier = identifier.lower().strip()
        for product in self.products:
            if product.name.lower().strip() == identifier:
                print("Your product is: " + product.name)
                return product
        return None

    # List all customers, showing detailed information about each
    def list_customers(self):
        for customer in self.customers:
            print(f"ID: {customer.ID}, Name: {customer.name}, Reward Points: {customer.reward}", end='')
            if isinstance(customer, VIPCustomer):
                print(f", Discount Rate: {customer.discount_rate}%")
            else:
                print()


    def compute_bundle_price(self, products):
        # Calculate the bundle price as 80% of the total price of all included products
        total_price = 0
        for pid in products:
            product = self.find_product_by_id(pid)
            if product is not None:
                total_price += product.price
        return "{:.2f}".format(float(0.8 * total_price))

    def bundle_prescription_requirement(self, products):
        for pid in products:
            product = self.find_product_by_id(pid)
            if product is not None and product.requires_prescription:
                return True
        return False

    def list_products(self):
        print("Products:")
        for product in self.products:
                print(f"ID: {product.ID}, Name: {product.name}, Price: {product.price} AUD, Prescription Requirement: {product.requires_prescription}")
        print("Bundles:")
        for bundle in self.bundles:
                print( f"Bundle ID: {bundle.ID}, Name: {bundle.name}, Price: {self.compute_bundle_price(bundle.products)} AUD, Products:{bundle.products}, Prescription Required: {self.bundle_prescription_requirement(bundle.products)}")

    def find_bundle(self, identifier):
        identifier = identifier.lower().strip()
        for bundle in self.bundles:
            if bundle.name.lower().strip() == identifier:
                print("Your Bundle is: " + bundle.name)
                return bundle
        return None

### Implementation of the custom exception classes in the validation class does not allow the program to wait until the user has given a correct input.

# class InvalidNameError(Exception):
#     """Exception raised for errors in the input of the name."""
#     pass
#
# class InvalidProductError(Exception):
#     """Exception raised for errors in the product input."""
#     pass
#
# class InvalidQuantityError(Exception):
#     """Exception raised for errors in the input quantity."""
#     pass
#
# class InvalidPrescriptionAnswerError(Exception):
#     """Exception raised for errors in the prescription answer."""
#     pass

class Validation:
    def __init__(self, records):
        self.records = records

    def validate_customer_name(self):
        while True:
            customer_name = input("Enter your name (alphabets only): ")
            if customer_name.isalpha():
                return customer_name
            else:
                print("Invalid name. Please use alphabets only.")

    def validate_product_input(self):
        while True:
            product_name = input("Enter the product/bundle name or ID you wish to purchase: ")
            product = self.records.find_product(product_name)
            if product:
                return ('product', product)
            bundle = self.records.find_bundle(product_name)
            if bundle:
                return ('bundle', bundle)
            print("Product not found. Please enter a valid product name.")

    def validate_quantity(self):
        while True:
            try:
                quantity = int(input("Enter quantity (positive integer): "))
                if quantity > 0:
                    return quantity
                else:
                    print("Quantity must be greater than zero.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def validate_prescription(self, product):
        if product.requires_prescription:
            while True:
                prescription = input("This product requires a prescription. Do you have one? (y/n): ")
                if prescription.lower() in ['y', 'n']:
                    if prescription.lower() == 'y':
                        return True
                    else:
                        print("You cannot purchase this product without a prescription.")
                        return False
                else:
                    print("Invalid response. Please enter 'y' for yes or 'n' for no.")
        return True

class Bundle:
    def __init__(self, ID, name, products, total_price, prescription_requirement):
        self.ID = ID
        self.name = name
        self.products = products  # List of products in the bundle
        self.price = total_price
        self.requires_prescription = prescription_requirement


# Operations Class to handle user interactions and operational logic
class Operations:
    def __init__(self, customer_file, product_file):
        self.records = Records()  # Load the records handling class
        self.validation = Validation(self.records)  # Initialize validation class
        self.load_data(customer_file, product_file)

    # Load customer and product data from specified files
    def load_data(self, customer_file, product_file):
        # Attempt to load customer and product data from files
        try:
            self.records.read_customers(customer_file)
            self.records.read_products(product_file)
        except Exception as e:
            print(f"Failed to load data: {e}")
            exit()

    # Display the main menu and handle user choices
    def display_menu(self):
        print("\nMenu:")
        print("1. Make a purchase")
        print("2. Display existing customers")
        print("3. Display existing products")
        print("4. Exit")
        choice = input("Enter your choice: ")
        self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice == '1':
            self.make_purchase()
        elif choice == '2':
            self.records.list_customers()
        elif choice == '3':
            self.records.list_products()
        elif choice == '4':
            print("Exiting program...")
            exit()
        else:
            print("Invalid choice. Please try again.")
        self.display_menu()  # Redisplay menu after handling choice

    # Facilitate the purchasing process including updating rewards and printing receipts
    def make_purchase(self):
        customer_name = self.validation.validate_customer_name()
        item_type, item = self.validation.validate_product_input()

        if item_type == 'bundle':
            if item.requires_prescription and not self.validation.validate_prescription(item):
                return
            quantity = self.validation.validate_quantity()

            customer = self.records.find_customer(customer_name)

            if customer is None:
                print("Customer not found. Please try again.")
                return

            bundle = item
            original_cost = float(bundle.price) * quantity
            discount = 0 if not isinstance(customer, VIPCustomer) else customer.get_discount(original_cost)
            total_cost = original_cost - discount
            reward = customer.get_reward(total_cost)
            customer.update_reward(reward)
        else:
            product = item
            if product.requires_prescription and not self.validation.validate_prescription(product):
                return
            quantity = self.validation.validate_quantity()

            customer = self.records.find_customer(customer_name)
            product = self.records.find_product(product.name)

            if customer is None or product is None:
                print("Your customer or product details cannot be found. Please try again.")
                return

            order = Order(customer, product, quantity)
            original_cost, discount, total_cost, reward = order.compute_cost()
            customer.update_reward(reward)

        # Print the receipt based on customer type and item type
        print("---------------------------------------------------------")
        print("Receipt")
        print("---------------------------------------------------------")
        print(f"Name: {customer.name}")
        if item_type == 'bundle':
            print(f"Bundle: {bundle.name}")
            print(f"Included Products: {', '.join([pid for pid in bundle.products])}")
        else:
            print(f"Product: {product.name}")
            print(f"Unit Price: {product.price} (AUD)")
            print(f"Quantity: {quantity}")
        print("---------------------------------------------------------")
        if isinstance(customer, VIPCustomer):
            print(f"Original cost: {original_cost} AUD")
            print(f"Discount: {discount} AUD")
        print(f"Total cost: {total_cost} AUD")
        print(f"Earned reward: {reward}")

    def run(self):
        self.display_menu()


if __name__ == '__main__':
    operations = Operations('./customers.txt', './products.txt')
    operations.run()

"""Developed in PyCharm Community Edition"""