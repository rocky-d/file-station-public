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
        ("USB Drive", 15),
    ],
    "Electronics": [
        ("Smart TV", 800),
        ("Bluetooth Speaker", 120),
        ("Camera", 500),
        ("Smartwatch", 200),
        ("Home Theater", 700),
        ("Gaming Console", 450),
    ],
    "Groceries": [
        ("Milk", 2),
        ("Bread", 1.5),
        ("Eggs", 3),
        ("Rice", 10),
        ("Chicken", 12),
        ("Fruits", 6),
        ("Vegetables", 5),
        ("Snacks", 8),
    ],
}


# Display the product categories
def display_sorted_products(products_list, sort_order):
    sorted_products = sorted(
        products_list, key=lambda x: x[1], reverse=(sort_order == "desc")
    )
    return sorted_products


# Display products in a selected category
def display_products(products_list):
    for i, (product, price) in enumerate(products_list, 1):
        print(f"{i}.{product} -${price}")


# Display product categories
def display_categories():
    print("Available Categories:")
    for i, categories in enumerate(products.keys(), 1):
        print(f"{i}.{categories}")
    choice = input("Please select a category by number 0 to Exit: ")
    if choice.isdigit() and 1 <= int(choice) <= len(categories):
        return int(choice) - 1
    else:
        return None


def add_to_cart(cart, product, quantity):
    cart.append(tuple(list(product) + [quantity]))


def display_cart(cart):
    total = 0
    for item in cart:
        product_name, price, quantity = item
        item_price = price * quantity
        total += item_price
        print(f"{product_name} - ${price} x {quantity} = ${item_price}")
    print(f"Total cost: ${total}")
    return total


def generate_receipt(name, email, cart, total_cost, address):
    print("--- Receipt ---")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Delivery Address: {address}")
    print("\nItems Purchased:")
    for item, quantity in cart:
        print(f"{item} x{quantity}")
    print(f"\nTotal Cost: ${total_cost}")
    print("Your items will be delivered in 3 days. Payment will be accepted after successful delivery.")


def validate_name(name):
    parts = name.split()
    return len(parts) == 2 and all(part.isalpha() for part in parts)


def validate_email(email):
    return "@" in email


def main():
    cart = []
    total_cost = 0

    # Ask user for name and email
    name = input("Enter your full name: ")
    while not validate_name(name):
        print("Invalid name. Please enter both first and last name.")
        name = input("Enter your full name: ")

    email = input("Enter your email address: ")
    while not validate_email(email):
        print("Invalid email. Please enter a valid email.")
        email = input("Enter your email address: ")

    while True:
        # Display categories
        category_choice = display_categories()
        if category_choice is None:
            break

        # Get selected category and show products
        category = list(products.keys())[category_choice - 1]
        print(f"\nYou selected {category}:\n")
        display_products(products[category])

        # Ask for product selection
        while True:
            choice = input(
                "1. Select a product to buy\n"
                "2. Sort products by price\n"
                "3. Go back to category selection\n"
                "4. Finish shopping\nChoose an option (number): "
            )

            if choice == "1":
                try:
                    product_choice = int(input("Enter the product number: "))
                    if product_choice < 1 or product_choice > len(products[category]):
                        raise ValueError
                    product = products[category][product_choice - 1]
                except ValueError:
                    print("Invalid product number. Please try again.")
                    continue

                quantity = int(input(f"How many {product[0]}s would you like to buy? "))
                add_to_cart(cart, product[0], quantity)
                total_cost += product[1] * quantity
                print(f"Added {quantity} x {product[0]} to cart.")

            elif choice == "2":
                sort_order = input("Enter 1 for ascending or 2 for descending: ")
                sorted_products = sorted(
                    products[category],
                    key=lambda x: x[1],
                    reverse="asc" if sort_order == "1" else "desc",
                )
                display_products(sorted_products)

            elif choice == "3":
                break

            elif choice == "4":
                if cart:
                    address = input("Enter your delivery address: ")
                    generate_receipt(name, email, cart, total_cost, address)
                else:
                    print("Thank you for using our portal. Hope you buy something next time. Have a nice day!")
                break


""" The following block makes sure that the main() function is called when the program is run. 
It also checks that this is the module that's being run directly, and not being used as a module in some other program. 
In that case, only the part that's needed will be executed and not the entire program """
if __name__ == "__main__":
    main()
