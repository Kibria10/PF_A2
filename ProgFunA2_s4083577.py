"""
Name: Maharab Kibria
ID: s4083577
Attempted Level: Pass Level. 19th May, 2024
Limitation Notice: The current implementation of the find_customer and find_product methods supports searching by customer ID and product ID only. There is an ongoing issue with searching by customer or product names using the dictionary approach. Despite attempts to normalize data through trimming and converting to lowercase, these searches are not returning expected results. I plan to resolve this issue in next submissions.

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
One significant challenge was managing the search functionality for customer and product names, which initially failed to handle cases and whitespace effectively. This required revisiting string handling and normalization, which was a valuable lesson in the importance of rigorous testing and user input validation.

"""
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
        print(f"ID: {self.ID}, Name: {self.name}, Reward Points: {self.reward}, Reward Rate: {BasicCustomer.reward_rate}%")

    # Class method to change the reward rate for all basic customers
    @classmethod
    def set_reward_rate(cls, new_rate):
        cls.reward_rate = new_rate

# Subclass for VIP customers with both reward and discount rates
class VIPCustomer(Customer):
    reward_rate = 100  # static variable shared by all VIPCustomer instances
    def __init__(self, ID, name, reward, discount_rate=8):
        super().__init__(ID, name, reward)
        self.discount_rate = discount_rate # Unique discount rate for VIP customers

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
        print(f"ID: {self.ID}, Name: {self.name}, Reward Points: {self.reward}, Reward Rate: {VIPCustomer.reward_rate}%, Discount Rate: {self.discount_rate}%")

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
        self.requires_prescription = requires_prescription == 'y'  # 'y' means prescription required

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
            discount = self.customer.get_discount(original_cost) # Calculate discount if customer is VIP
            total_cost = original_cost - discount
        else:
            discount = 0
            total_cost = original_cost
        reward = self.customer.get_reward(total_cost) # Calculate reward points earned from the transaction
        return original_cost, discount, total_cost, reward


# Records Class to manage data operations
class Records:
    def __init__(self):
        self.customers = []
        self.products = []

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
                    if len(parts) == 4:  # Check if the product line has the correct format
                        product_id, product_name, price, prescription_required = parts
                        self.products.append(Product(product_id, product_name, float(price), prescription_required))
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred while reading product data: {e}")

    # Search for a customer by ID or name, returning the customer object if found
    def find_customer(self, identifier):
        identifier = identifier.lower().strip() # Trim whitespace and convert to lowercase
        for customer in self.customers:
            if customer.name.lower().strip() == identifier:
                print("Hello "+ customer.name)
                return customer
        return None

    # Search for a product by ID or name, returning the product object if found
    def find_product(self, identifier):
        identifier = identifier.lower().strip() # Trim whitespace and convert to lowercase
        for product in self.products:
            if product.name.lower().strip() == identifier:
                print("Your product is: "+ product.name)
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

    # List all products, showing detailed information about each
    def list_products(self):
        for product in self.products:
            print(f"ID: {product.ID}, Name: {product.name}, Price: {product.price} AUD")


# Operations Class to handle user interactions and operational logic
class Operations:
    def __init__(self, customer_file, product_file):
        self.records = Records() # Instantiate the Records class to manage data
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
        customer_name = input("Your name: ")
        product_name = input("What would you like to buy today?: ")
        quantity = int(input("Quantity: "))
        # customer_name = "B1"
        # product_name = "P1"
        # quantity = 1

        customer = self.records.find_customer(customer_name)
        product = self.records.find_product(product_name)

        if customer is None or product is None:
            print("Customer or product not found. Please try again.")
            return

        order = Order(customer, product, quantity)
        original_cost, discount, total_cost, reward = order.compute_cost()

        # Update customer reward
        customer.update_reward(reward)

        # Print the receipt based on customer type
        if isinstance(customer, VIPCustomer):
            print("---------------------------------------------------------")
            print("Receipt")
            print("---------------------------------------------------------")
            print(f"Name: {customer.name}")
            print(f"Product: {product.name}")
            print(f"Unit Price: {product.price} (AUD)")
            print(f"Quantity: {quantity}")
            print("---------------------------------------------------------")
            print(f"Original cost: {original_cost} (AUD)")
            print(f"Discount: {discount} (AUD)")
            print(f"Total cost: {total_cost} (AUD)")
            print(f"Earned reward: {reward}")
        else:
            print("---------------------------------------------------------")
            print("Receipt")
            print("---------------------------------------------------------")
            print(f"Name: {customer.name}")
            print(f"Product: {product.name}")
            print(f"Unit Price: {product.price} (AUD)")
            print(f"Quantity: {quantity}")
            print("---------------------------------------------------------")
            print(f"Total cost: {total_cost} (AUD)")
            print(f"Earned reward: {reward}")

    def run(self):
        self.display_menu()


if __name__ == '__main__':
    operations = Operations('./customers.txt', './products.txt')
    operations.run()


"""Developed in PyCharm Community Edition"""