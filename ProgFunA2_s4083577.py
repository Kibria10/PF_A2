"""
Name: Maharab Kibria
ID: s4083577
Attempted Level: HD Level. 28th May, 2024

VCS: Git (Github: https://github.com/Kibria10/PF_A2/tree/pass_level) // My work with commits are recorded and I have created 4 branches with the level names for each stage of the assignment.
//I will make this repository public after submission. 

Limitations:
The program has filled up all the requirements till credit level.
In DI_Level it has not filled up requirement i > allowing multiple products and quantities in one order
In HD_Level it has not filled up requirement vi > while terminating, files will be updated.
Aside of this, as far as I have tested this program with different scenarios in different levels, it has met the requirements and followed the business logics.

***Design Process and Coding Steps:
I aimed to keep the SOLID principles in mind, adapting them as much as possible to a Python environment. The class structures were clearly outlined in our project specifications, which provided a solid foundation.
Initially, I started by defining the necessary classes and sketching out the methods. I didn't write all the method implementations right away but instead commented on what each method should achieve. This preliminary setup was incredibly useful later on, as it guided me when fleshing out the details.
After setting up the basic structures, I moved on to create the Operations class. This was crucial for achieving the "Pass Level" goals as it tied all the components together. Running the initial tests revealed some gaps since many methods were still placeholders.
I then systematically filled in these methods, paying close attention to the project documentation to ensure that the implementation met the specific needs of VIP and basic customers, as well as the order handling process. This phase required careful attention to detail to adhere to the business logic outlined in our guidelines.
The next step involved handling file input and output, which proved challenging. I spent quite some time getting this right, but resources like the Python I/O documentation (https://docs.python.org/3/tutorial/inputoutput.html) were incredibly helpful, offering many practical examples.
Finally, I focused on implementing the functionality to display customer and product data effectively and enabling the process to purchase products after loading data from files. This last part brought everything together, allowing for a full demonstration of the system's capabilities.
Throughout this process, I iterated over the code, refining and testing repeatedly, which helped in ironing out the bugs.

***Code Analysis:
Use of Class Methods and Static Variables: For the BasicCustomer and VIPCustomer classes, static variables and class methods (like set_reward_rate) are used to manage properties shared across all instances. This approach ensures that changes to reward rates affect all customers of a type globally, which is more efficient than updating each instance individually.
Polymorphism in Customer Subclasses: Methods like get_reward and get_discount are implemented differently across subclasses to reflect the differing behaviors between basic and VIP customers, providing flexibility in how different types of customers are treated.
Error Handling in File Operations: Robust error handling in the Records class prevents the program from crashing due to file-related errors, ensuring a graceful exit or error message is presented to the user.
Iterative Approach in Operations Class: The loop within display_menu and recursive call to handle_choice demonstrate an iterative approach to handle user inputs continuously until the exit option is selected.

***Challenges:
1. Coding in a single file. As the assignment requirement, it has been difficult to write multiple classes into a single file and follow up.
2. Increase of methods. As the levels were increasing, I had to create few similar methods that may not have been ideal.
3. Implementation of Encapsulation has been challenging with the increase of levels.

"""


import sys

def main():
    # Default file names
    customer_file = 'customers.txt'
    product_file = 'products.txt'
    order_file = 'orders.txt'  # Default file name for orders

    # Check the number of command line arguments
    argc = len(sys.argv)
    if argc == 4:
        # Command line provides all three filenames
        customer_file, product_file, order_file = sys.argv[1], sys.argv[2], sys.argv[3]
    elif argc == 3:
        # Only customer and product files provided
        customer_file, product_file = sys.argv[1], sys.argv[2]
    elif argc == 1:
        # No arguments provided, use default files
        print("Using default file names.")
    else:
        # Incorrect number of arguments provided
        print("Usage: python script.py [customer_file] [product_file] [order_file]")
        sys.exit(1)
    # Initialize and run the operations
    operations = Operations(customer_file, product_file, order_file)
    operations.run()

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
        return total_cost * (self.discount_rate)

    # Calculate reward, considering the discount applied
    def get_reward(self, total_cost):
        return round((total_cost - self.get_discount(total_cost)) * VIPCustomer.reward_rate/100)

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

#HD Level// Redefining a new OrderHistory class to keep the business logics seperate and handling the functions in ease
class OrderHistory:
    def __init__(self, customer, products, total_cost, earned_rewards, date):
        self.customer = customer
        self.products = products  # List of tuples (product, quantity)
        self.total_cost = total_cost
        self.earned_rewards = earned_rewards
        self.date = date

    def display(self):
        print(
            f"Date: {self.date}, Customer: {self.customer.name}, Total Cost: {self.total_cost}, Earned Rewards: {self.earned_rewards}")
        for product, quantity in self.products:
            print(f"    Product: {product.name}, Quantity: {quantity}")

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
        self.orders = []


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

    def read_orders(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    customer = self.find_customer(parts[0])
                    products = [(self.find_product(parts[i]), int(parts[i + 1])) for i in range(1, len(parts) - 3, 2)]
                    total_cost = float(parts[-3])
                    earned_rewards = int(parts[-2])
                    date = parts[-1]
                    if customer and products:
                        self.orders.append(OrderHistory(customer, products, total_cost, earned_rewards, date))
                    else:
                        print("Error: Customer or products not found in file.")
        except FileNotFoundError:
            print("Cannot load the order file")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Search for a customer by ID or name, returning the customer object if found
    def find_customer(self, identifier):
        identifier = identifier.lower().strip().lstrip()  # Trim whitespace and convert to lowercase
        for customer in self.customers:
            if customer.name.lower().strip().lstrip() == identifier or customer.ID.lower().strip().lstrip() == identifier:
                return customer
        return None

    def find_product_by_id(self, product_id): ##TO DO: Merge this method with the other one
        # Search in single products
        for product in self.products:
            if product.ID == product_id.strip().lstrip():
                return product
        return None

    # Search for a product by ID or name, returning the product object if found
    def find_product(self, identifier):
        identifier = identifier.lower().strip().lstrip()
        for product in self.products:
            if product.ID.lower().strip().lstrip() == identifier or product.name.lower().strip().lstrip() == identifier:
                return product
        for bundle in self.bundles:
            if bundle.ID.lower().strip().lstrip() == identifier or bundle.name.lower().strip().lstrip() == identifier:
                return bundle
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

    def add_update_product(self, product_id, name, price, requires_prescription):
        existing_product = self.find_product_by_id(product_id)
        if existing_product:
            existing_product.name = name
            existing_product.price = price
            existing_product.requires_prescription = requires_prescription == 'y'
        else:
            self.products.append(Product(product_id, name, price, requires_prescription))
        print("Product information updated successfully.")

class Validation:
    def __init__(self, records):
        self.records = records

    def validate_customer_name(self):
        while True:
            customer_input = input("Enter your name or ID: ")
            # Check if the input contains only alphabets for name or alphanumeric for IDs
            if customer_input.isalpha():
                return customer_input
            elif customer_input.isalnum() and not customer_input.isalpha():
                return customer_input
            else:
                print("Invalid input. Please use alphabets only for names or alphanumeric characters for IDs.")

    def validate_product_input(self):
        while True:
            item_name = input("Enter the product/bundle name or ID you wish to purchase: ")
            item = self.records.find_product(item_name)
            if item:
                # Check if the item is a bundle by looking for the 'products' attribute
                if hasattr(item, 'products'):
                    return ('bundle', item)
                else:
                    return ('product', item)
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
    def __init__(self, customer_file, product_file, order_file=None):
        self.records = Records()  # Load the records handling class
        self.validation = Validation(self.records)  # Initialize validation class
        self.load_data(customer_file, product_file, order_file)

    # Load customer and product data from specified files
    def load_data(self, customer_file, product_file, order_file):
        # Attempt to load customer and product data from files
        try:
            self.records.read_customers(customer_file)
            self.records.read_products(product_file)
            if order_file:  # Load orders only if the filename is provided
                self.records.read_orders(order_file)
        except Exception as e:
            print(f"Failed to load data: {e}")
            exit()

    # Display the main menu and handle user choices
    def display_menu(self):
        print("\nMenu:")
        print("1. Make a purchase")
        print("2. Display existing customers")
        print("3. Display existing products")
        print("4. Add/update product information")
        print("5. Adjust reward rate for Basic Customers")
        print("6. Adjust discount rate for VIP Customers")
        print("7. Display all orders")
        print("8. Display a customer order history")
        print("9. Exit")
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
            self.add_update_product_info()
        elif choice == '5':
            self.adjust_basic_customers_reward_rate()
        elif choice == '6':
            self.adjust_vip_customer_discount_rate()
        elif choice == '7':
            self.display_all_orders()
        elif choice == '8':
            self.display_customer_order_history()
        elif choice == '9':
            print("Exiting program...")
            exit()
        else:
            print("Invalid choice. Please try again.")
        self.display_menu()  # Redisplay menu after handling choice

    def add_update_product_info(self):
        product_id = input("Enter the product ID: ")
        name = input("Enter the product name: ")
        price = input("Enter the product price (AUD): ")
        requires_prescription = input("Does the product require a prescription? (y/n): ")

        try:
            price = float(price)  # Ensure the price is a valid float
            self.records.add_update_product(product_id, name, price, requires_prescription)
        except ValueError:
            print("Invalid input for price. Please enter a valid number.")

    def adjust_basic_customers_reward_rate(self):
        while True:
            try:
                new_rate = float(input("Enter new reward rate (as a decimal for percentage, e.g., 1 for 100%): "))
                if new_rate <= 0:
                    raise ValueError("Reward rate must be positive.")
                BasicCustomer.set_reward_rate(new_rate * 100)
                print("Reward rate updated for all Basic customers.")
                break
            except ValueError as e:
                print(f"Invalid input: {str(e)}. Please try again.")

    def adjust_vip_customer_discount_rate(self):
        while True:
            customer_id_or_name = input("Enter the VIP customer's ID or name: ")
            customer = self.records.find_customer(customer_id_or_name)
            if isinstance(customer, VIPCustomer):
                try:
                    new_discount_rate = float(input("Enter new discount rate (e.g., 0.2 for 20%): "))
                    if new_discount_rate < 0:
                        raise ValueError("Discount rate cannot be negative.")
                    customer.set_discount_rate(new_discount_rate)
                    print("Discount rate updated for the VIP customer.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {str(e)}. Please try again.")
            else:
                print("Invalid customer or not a VIP customer. Please try again.")

    # Facilitate the purchasing process including updating rewards and printing receipts
    def make_purchase(self):
        customer_name = self.validation.validate_customer_name()
        item_type, item = self.validation.validate_product_input()
        quantity = self.validation.validate_quantity()

        customer = self.records.find_customer(customer_name)
        if customer is None:
            print("Customer not found. Please try again.")
            return

        if item.requires_prescription and not self.validation.validate_prescription(item):
            return

        if item_type == 'bundle':
            self.handle_bundle_purchase(item, quantity, customer)
        else:
            self.handle_product_purchase(item, quantity, customer)

    def handle_bundle_purchase(self, bundle, quantity, customer):
        original_cost = float(bundle.price) * quantity
        discount = self.calculate_discount(customer, original_cost)
        total_cost = original_cost - discount
        reward = customer.get_reward(total_cost)
        customer.update_reward(reward)
        self.print_receipt(customer, 'bundle', bundle, quantity, original_cost, discount, total_cost, reward)

    def handle_product_purchase(self, product, quantity, customer):
        product = self.records.find_product(product.name)
        if product is None:
            print("Product details cannot be found. Please try again.")
            return

        order = Order(customer, product, quantity)
        original_cost, discount, total_cost, reward = order.compute_cost()
        customer.update_reward(reward)
        self.print_receipt(customer, 'product', product, quantity, original_cost, discount, total_cost, reward)

    def calculate_discount(self, customer, cost):
        if isinstance(customer, VIPCustomer):
            return customer.get_discount(cost)
        return 0

    def display_all_orders(self):
        if not self.records.orders:
            print("No historical orders to display.")
            return
        for order in self.records.orders:
            order.display()

    def display_customer_order_history(self):
        customer_name = input("Enter the customer's name to display their order history: ")
        customer = self.records.find_customer(customer_name)
        print(f"{customer.ID}")
        if not customer:
            print(f"No customer found with the name: {customer_name}")
            return

        # Filter orders for the specified customer
        customer_orders = [order for order in self.records.orders if order.customer.name == customer_name]
        if not customer_orders:
            print("No orders found for this customer.")
            return

        print(f"Order History of {customer_name}:")
        print(f"{'Order #':<10}{'Products':<30}{'Total Cost':<15}{'Earned Rewards':<15}")
        for i, order in enumerate(customer_orders, 1):
            product_details = ', '.join([f"{qty} x {prod.name}" for prod, qty in order.products])
            print(f"{i:<10}{product_details:<30}${order.total_cost:<14.2f}{order.earned_rewards:<15}")

    def print_receipt(self, customer, item_type, item, quantity, original_cost, discount, total_cost, reward):
        print("---------------------------------------------------------")
        print("Receipt")
        print("---------------------------------------------------------")
        print(f"Name: {customer.name}")
        if item_type == 'bundle':
            print(f"Bundle: {item.name}")
            print(f"Included Products: {', '.join([pid for pid in item.products])}")
        else:
            print(f"Product: {item.name}")
            print(f"Unit Price: {item.price} (AUD)")
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
    main()

"""Developed in PyCharm Community Edition"""