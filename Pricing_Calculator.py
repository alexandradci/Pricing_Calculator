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


def apply_discount(discount_tiers):
    def decorator(calculate_func):
        def wrapper(order, products):
            summary = calculate_func(order, products)
            total_with_tax = summary['total_with_tax']
            discount = 0
            discount_percentage = "0%"

            for threshold, rate in discount_tiers:
                if total_with_tax >= threshold:
                    discount = total_with_tax * rate
                    discount_percentage = f"{int(rate * 100)}%"
                    break

            summary['discount'] = discount
            summary['final'] = total_with_tax - discount
            summary['discount_percentage'] = discount_percentage
            return summary
        return wrapper
    return decorator

@apply_discount(discount_tiers=[(200, 0.2), (100, 0.1)])
def calculate_total_base(order, products):
    """Calculates the subtotal and tax."""
    calculate_subtotal = lambda order, prods: sum(prods[item] * qty for item, qty in order)
    subtotal = calculate_subtotal(order, products)
    tax_rate = 0.19
    calculate_tax = lambda sub, rate: sub * rate
    tax = calculate_tax(subtotal, tax_rate)
    total_with_tax = subtotal + tax

    return {
        'subtotal': subtotal,
        'tax': tax,
        'total_with_tax': total_with_tax,
        'order': order
    }

# print the receipt
def print_receipt(summary):
    print("\n--- Receipt ---")
    print_receipt_rec(summary['order'], summary, 0)  
    print("Thank you for shopping!\n")

def print_receipt_rec(order_items, summary, index):
    if index < len(order_items):
        item, qty = order_items[index]
        print(f"{item} x{qty} = {products[item] * qty:.2f}€")
        print_receipt_rec(order_items, summary, index + 1)  
    else:  # Base case: all items printed
        print(f"Subtotal: {summary['subtotal']:.2f}€")
        print(f"Tax (19%): {summary['tax']:.2f}€")
        print(f"Total with tax: {summary['total_with_tax']:.2f}€")
        print(f"Discount: {summary['discount']:.2f}€")
        print(f"Discount percentage: {summary['discount_percentage']}")
        print(f"Final total: {summary['final']:.2f}€")

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
summary = calculate_total_base(order, products)

# ask if the user wants a receipt
def get_receipt_choice():
    while True:
        message = input("Do you want to print a receipt? (yes/no): ").strip().lower()
        is_valid_input = lambda x: x in ("yes", "no")  
        if is_valid_input(message):
            return message
        else:
            print("Incorrect input! Please enter yes or no.")

receipt_choice = get_receipt_choice()

if receipt_choice == "yes":
    print_receipt(summary)
elif receipt_choice == "no":
    print("Goodbye!")
