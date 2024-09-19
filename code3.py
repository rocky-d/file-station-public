# Products available in the store by category
products = {
    "IT Products": [
        ("Laptop", 1000),
        ("Smartphone", 600),
        ("Headphones", 150),
        ("Keyboard", 50),
        ("Monitor", 300),
        ("Mouse", 25),
        ("Printer", 120),
        ("USB Drive", 15)
    ],
    "Electronics": [
        ("Smart TV", 800),
        ("Bluetooth Speaker", 120),
        ("Camera", 500),
        ("Smartwatch", 200),
        ("Home Theater", 700),
        ("Gaming Console", 450)
    ],
    "Groceries": [
        ("Milk", 2),
        ("Bread", 1.5),
        ("Eggs", 3),
        ("Rice", 10),
        ("Chicken", 12),
        ("Fruits", 6),
        ("Vegetables", 5),
        ("Snacks", 8)
    ]
}


def display_categories():
    for index, category in enumerate(products, start=1):
        print(f"[{index}] {category}")
    choice = input("Please select a category: ")
    if choice.isdigit() and 0 <= int(choice) - 1 <= len(products) - 1:
        return int(choice) - 1
    return None


def display_products(products_list):
    for index, (product, price) in enumerate(products_list, start=1):
        print(f"{index}. {product} - ${price}")


def display_sorted_products(products_list, sort_order):
    if sort_order == "desc":
        sorted_list = sorted(products_list, key=lambda x: x[1], reverse=True)
    if sort_order == "asc":
        sorted_list = sorted(products_list, key=lambda x: x[1], reverse=False)
    display_products(sorted_list)
    return sorted_list


def add_to_cart(cart, product, quantity):
    cart.append((product[0], product[1], quantity))


def display_cart(cart):
    total_cost = 0
    for product, price, quantity in cart:
        cost = price * quantity
        total_cost += cost
        print(f"{product} - ${price} x {quantity} = ${cost}")
    print(f"Total cost: ${total_cost}")


def generate_receipt(name, email, cart, total_cost, address):
    print(f"Customer: {name}")
    print(f"Email: {email}")
    print("Items Purchased:")
    for product, price, quantity in cart:
        print(f"{quantity} x {product} - ${price} = ${price * quantity}")
    print(f"Total: ${total_cost}")
    print(f"Delivery Address: {address}")
    print("Your items will be delivered in 3 days.")
    print("Payment will be accepted upon delivery.")


def validate_name(name):
    return len(name.split(" ")) == 2 and all(part.isalpha() for part in name.split())


def validate_email(email):
    return "@" in email


def main():
    name = input("Please enter your name: ")
    while not validate_name(name):
        name = input("Please enter your name: ")

    email = input("Please enter your e-mail: ")
    while not validate_email(email):
        email = input("Please enter your e-mail: ")

    cart = []
    while True:
        cate = display_categories()
        if cate is None:
            continue

        cate = list(products.keys())[cate]
        prod = products[cate]

        display_products(prod)

        print("Options:")
        print("1. Select a product to buy")
        print("2. Sort the products according to the price")
        print("3. Go back to the category selection")
        print("4. Finish shopping")

        opt = input("Choose an option: ")

        if opt == "1":

            product_choice = input("Enter the number of the product you want to buy: ")
            product_index = int(product_choice) - 1
            if 0 <= product_index < len(prod):
                quantity = input("Enter the quantity: ")
                if quantity.isdigit() and int(quantity) > 0:
                    add_to_cart(cart, prod[product_index], int(quantity))
                else:
                    print("Invalid quantity.")
            else:
                print("Invalid product number.")

        elif opt == "2":

            order = input("Sort by price: 1 for ascending, 2 for descending: ")
            if order == "1":
                display_sorted_products(prod, "asc")
            elif order == "2":
                display_sorted_products(prod, "desc")
            else:
                print("Invalid option.")

        elif opt == "3":

            continue

        elif opt == "4":

            if 1 <= (cart):
                display_cart(cart)
                address = input("Enter delivery address: ")
                total = sum(price * quantity for prod, price, quantity in cart)
                generate_receipt(name, email, cart, total, address)
            else:
                print("Thank you for using our portal. Hope you buy something from us next time. Have a nice day.")
            break

    print("Byebye!")

""" The following block makes sure that the main() function is called when the program is run. 
It also checks that this is the module that's being run directly, and not being used as a module in some other program. 
In that case, only the part that's needed will be executed and not the entire program """
if __name__ == "__main__":
    main()
