# imports attribute getter and tabulate modules
from operator import attrgetter
from tabulate import tabulate

# Sets formating values
RED = '\033[91m'
COLRESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[92m'
ITALIC = '\033[3m'


#========The beginning of the class==========
# Defines class Shoe
class Shoe:

    # initiates values for country, code, product, cost and quantity
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
    # Function to return cost    
    def get_cost(self):
        return self.cost
        
    # Function to return quantity    
    def get_quantity(self):
        return self.quantity

    # Function to return string description of an intem    
    def __str__(self):
        shoe_details = f"{self.country},{self.code},"\
                       f"{self.product},{self.cost},"\
                       f"{self.quantity}"

        return shoe_details

    # Function to update item quantity                       
    def change_guantity(self, new_qty): 
        self.quantity = new_qty 
        print(f"{GREEN}Quantity for {BOLD}{self.product}{COLRESET} "
              f"{GREEN}has been updated to {BOLD}{new_qty}{COLRESET} \n")
        
    # Function to update item cost
    def change_cost(self, new_cost): 
        self.cost = new_cost
        print(f"{GREEN}Price for {BOLD}{self.product}{COLRESET} "
              f"{GREEN}has been updated to {BOLD}{new_cost}{COLRESET} \n")



#=============Shoe list===========

# Initiates empty list to store Shoe class objects
shoe_list = []

# Initiates empty list to store shoe description for tabulatation
table_list=[]
    

#==========Functions outside the class==============

# This function reads the inventory file, skips first line with header 
# Adds all class objects to the shoe_list list
def read_shoes_data():
    shoe_list.clear()
    with open("inventory.txt", "r") as f:
        i_file = f.readlines()[1:]
        for line in i_file:
            line = line.strip("\n")
            element = line.split(",")

            # This makes sure cost and quantity values are in correct format
            try:
                shoe_list.append(Shoe(element[0], 
                                      element[1], 
                                      element[2], 
                                      int(element[3]), 
                                      int(element[4])))
            except ValueError:
                print(f"{RED}{element[2]} details are incorrect \n{COLRESET}")
                
    
# Function to add new shoe           
def capture_shoes(): 
    while True:

        # Requests input from user and errors if incorrect type
        try:
            print(f"\t{BOLD} *** Enter details *** {COLRESET}")
            s_country = str(input("Country: \t"))
            s_code = str("SKU"+input("Product code: \tSKU"))
            s_product = str(input("Product name: \t"))
            s_cost = int(input("Cost: \t\t"))
            s_quantity = int(input("Quantity: \t"))
            
            # Opens file and adds new shoe details in a new line
            with open("inventory.txt", "a") as f:
                f.write(f"\n{s_country},{s_code},"
                        f"{s_product},{s_cost},{s_quantity}")
            print(f"{GREEN}{s_product} added to stock. \n{COLRESET}")
            break
        except ValueError:
            print(f"{RED}Please type correct details \n{COLRESET}")


# Function to update file with values from the list
def update_file():

    # Adds header to the file
    with open("inventory.txt", "w") as f:
        f.write("Country,Code,Product,Cost,Quantity")

    # Adds all shoes details to the file    
    with open("inventory.txt", "a") as f:
        for i in shoe_list:
            f.write(f"\n{i.__str__()}")
        

    
# Function to display all shoes details
def view_all():

    # Refreshes shoe_list with data from file
    shoe_list.clear()
    read_shoes_data()
    
    # Refreshes table_list list with shoe details 
    # Uses __str__ function
    table_list.clear()
    for Shoe in shoe_list:
        shoe_details = Shoe.__str__().strip()
        shoe_details = shoe_details.split(",")
        element = shoe_details
        table_list.append(element)
    
    # Prints all shoes details from table_list in a table
    header = "Country","Code","Product","Cost","Quantity"
    shoe_table = tabulate(table_list, headers=header, tablefmt="fancy_grid")
    print(f"{BOLD} \t\t\t*** All Items *** {COLRESET}")
    print(f"{shoe_table} \n")

   
# Function to update stock value for lowest stocked item
def re_stock():

    # Refreshes shoe_list list
    shoe_list.clear()
    read_shoes_data()
    
    # Finds item with lowest stock quantity and prints details
    min_attr = min(shoe_list, key=attrgetter('quantity'))
    min_item_code = min_attr.code
    print(f"The shoe low in stock is: \t{BOLD}{min_attr.product} \n{COLRESET}"
          f"Current stock is: \t\t{BOLD}{min_attr.quantity} \n{COLRESET}")

    # Asks for new quantity for the item & updates in the list
    # Then updates inventory file with new values
    new_qty = int(input("Please enter new stock value for this item: \n"))
    for i in shoe_list:
        if i.code == min_item_code:
            i.change_guantity(new_qty)
            break
    update_file()


# Function to update stock value for highest stocked item
def highest_qty():
    
    # Refreshes shoe_list list
    shoe_list.clear()
    read_shoes_data()
    
    # Finds item with highest stock quantity and prints details
    max_attr = max(shoe_list, key=attrgetter('quantity'))
    max_item_code = (max_attr.code)
    print("The shoe high in stock is: "
          f"\t{BOLD}{max_attr.product}{COLRESET} \n"
          "Current cost is: "
          f"\t\t{BOLD}{max_attr.cost}{COLRESET} \n")
    
    # Asks for new cost for the item & updates in the list
    # Then updates file with new values
    new_cost = int(input("Enter a new cost for this item: "))
    for i in shoe_list:
        if i.code == max_item_code:
            i.change_cost(new_cost)
            break
    update_file()


# Function to find a shoe
def search_shoe():

    # Refreshes list
    shoe_list.clear()
    read_shoes_data()

    # Asks user if they want to search by product code or name
    while True:
        try:
            search_type = int(input("""Do you want to serach by:
    1 - product code
    2 - product name
    """))

            # Searches product by code
            # Requests product code & prints shoe details
            if search_type == 1:
                search_code = input("Please enter product code: \t")

                for i in shoe_list:
                    if i.code == search_code:
                        print(f"\n\t*** Shoe details *** \n"
                              f"Country: \t{i.country}\n"
                              f"Code: \t\t{i.code}\n"
                              f"Product: \t{i.product}\n" 
                              f"Cost: \t\t{i.cost}\n"
                              f"Quantity: \t{i.quantity}\n")
                break

            # Searches product by name
            # Requests product name & prints shoe details
            elif search_type == 2:
                search_name = input("Please enter product name: \t")
                
                for i in shoe_list:
                    if i.product == search_name:
                        print(f"\n\t*** Shoe details *** \n"
                              f"Country: \t{i.country}\n"
                              f"Code: \t\t{i.code}\n"
                              f"Product: \t{i.product}\n" 
                              f"Cost: \t\t{i.cost}\n"
                              f"Quantity: \t{i.quantity}\n")
                break

            # Error message if cannot find product
            else:
                print(f"{RED}Unable to find this product \n{COLRESET}")

        # Error message if search type isn't integer
        except ValueError:   
            print(f"{RED}Please enter correct value \n{COLRESET}")


# Function to print stock value of all items
def value_per_item():

    # Refreshes list
    shoe_list.clear()
    read_shoes_data()

    # Prints all shoe details and it's stock value
    print(f"\n\t *** Shoe details ***")
    for i in shoe_list:
        value = i.get_quantity() * i.get_cost()
        print(f"{i.product} stock value is {value}")
    print("\n")
    
    
#==========Main Menu=============
while True:

    # Presents menu to the user and asks for input
    menu = input(str(f"""{BOLD} \t *** MENU *** {COLRESET}
{ITALIC}Please select from the following options {COLRESET}
  all - to see all inventory
  new - add new to inventory
  re-stock - find items to restock
  search - find specific item
  stock value - display stock value for all items
  sale - show overstocked items for sale  
  exit - to close the program
\n"""))
    
    # Prints all shoes details
    if menu == "all":
        view_all()

    # Adds new shoe
    elif menu == "new":
        capture_shoes()

    # Prints lowest stocked item and updates it's quantity
    elif menu == "re-stock":
        re_stock()

    # Searches for a shoe
    elif menu == "search":
        search_shoe()

    # Prints stock value of all shoes    
    elif menu == "stock value":
        value_per_item()

    # Prints details of highest stocked item and updates it's price
    elif menu == "sale":
        highest_qty()

    # Exists file
    elif menu == "exit":
        print(f"{ITALIC}Goodbye!{COLRESET}")
        exit()

    # Error when incorrect value is entered
    else:
        print(f"{RED} \nPlease select correct option. {COLRESET} \n")

    