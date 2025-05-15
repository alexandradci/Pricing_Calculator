import json

def log_attempt(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        #print(f"[LOGIN LOG] {func.__name__} returned: {result}") #debugging
        return result
    return wrapper

@log_attempt
def login(**kwargs):
    retries = kwargs.get("retries", 3)

    for attempt in range(retries):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Use filter to find user
        user = list(filter(lambda u: u["username"] == username and u["password"] == password, users))

        if user:
            print(f"✅ Welcome, {username}!")
            return True
        else:
            print("❌ Incorrect username or password.")

    print("🚫 Too many failed attempts. Exiting.")
    return False

# load products from a JSON file
def load_products():
    with open("products.json", "r") as file:
        data = json.load(file)
        users = data["users"]
        products_raw = data["products"]

        products_dict = {}
        for product in products_raw:
            for name, price in product.items():
                products_dict[name] = float(price)
        return products_dict, users

# load products
products, users = load_products()

# print available products
print("Available products:")
for name, price in products.items():
    print(f"- {name}: {price}€")
print()  # empty line for spacing

# save products
def save_products(products, users):
    prod_list = [{k: str(v)} for k, v in products.items()]
    with open("products.json", "w") as file:
        json.dump({"users": users, "products": prod_list}, file, indent=2)


# calculate the total with tax and discount
def calculate_total(order, products):
    subtotal = sum(products[item] * qty for item, qty in order)
    tax = subtotal * 0.19
    total_with_tax = subtotal + tax

    if total_with_tax >= 200:
        discount = total_with_tax * 0.2
        discount_percentage = "20%"
    elif total_with_tax >= 100:
        discount = total_with_tax * 0.1
        discount_percentage = "10%"
    else:
        discount = 0
        discount_percentage = "0%"

    return {
        'subtotal': subtotal,
        'tax': tax,
        'total_with_tax': total_with_tax,
        'discount': discount,
        'final': total_with_tax - discount,
        'order': order,
        'discount_percentage': discount_percentage
    }

# print the receipt
def print_receipt(summary):
    print("\n--- Receipt ---")
    for item, qty in summary['order']:
        print(f"{item} x{qty} = {products[item] * qty:.2f}€")
    print(f"Subtotal: {summary['subtotal']:.2f}€")
    print(f"Tax (19%): {summary['tax']:.2f}€")
    print(f"Total with tax: {summary['total_with_tax']:.2f}€")
    print(f"Discount: {summary['discount']:.2f}€")
    print(f"Discount percentage: {summary['discount_percentage']}")
    print(f"Final total: {summary['final']:.2f}€")
    print("Thank you for shopping!\n")

# program starts
if login(retries=3):
    # proceed to shopping
    print("Starting the shopping program...\n")
    # ... shopping code starts here ...
else:
    exit()

order = []

while True:
    prod = input("Enter the name of product: ")
    if prod in products:
        quant_input = input(f"Enter the quantity of {prod}: ")
        if quant_input.isdigit():
            quant = int(quant_input)
            order.append((prod, quant))
        else:
            print("Please enter a valid number.")
            continue
    else:
        print("Product not found.")
        continue

    add_more = input("Do you want to add more items? Enter 'yes' or 'no': ").strip().lower()
    if add_more == 'yes':
        continue
    elif add_more == 'no':
        break
    else:
        print("Invalid input, assuming 'no'.")
        break

# calculate total
summary = calculate_total(order, products)

# ask if the user wants a receipt
while True:
    message = input("Do you want to print a receipt? (yes/no): ").strip().lower()
    if message == "yes":
        print_receipt(summary)
        break
    elif message == "no":
        print("Goodbye!")
        break
    else:
        print("Incorrect input! Please enter yes or no.")
