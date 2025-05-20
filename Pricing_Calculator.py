from faker import Faker
import json
import random

fake = Faker()

clothing_types = ["T-shirt", "Dress", "Jeans", "Jacket", "Sweater", "Cap", "Skirt", "Hoodie", "Blouse", "Shorts"]
brands = ["Zara", "H&M", "Nike", "Adidas", "Puma", "Levi's"]

def log_attempt(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_attempt
def login(**kwargs):
    retries = kwargs.get("retries", 3)
    for attempt in range(retries):
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = list(filter(lambda u: u["username"] == username and u["password"] == password, users))
        if user:
            print(f"✅ Welcome, {username}!")
            return True
        else:
            print("❌ Incorrect username or password.")
    print("🚫 Too many failed attempts. Exiting.")
    return False

def generate_fake_clothes(n, starting_id=1):
    products = []
    for i in range(n):
        name = f"{fake.color_name()} {random.choice(brands)} {random.choice(clothing_types)}"
        price = str(random.randint(10, 100))
        product_id = f"{starting_id + i:04d}"
        product = {
            "id": product_id,
            "name": name,
            "price": price
        }
        products.append(product)
    return products

def load_products():
    with open("products.json", "r") as file:
        data = json.load(file)
        users = data["users"]
        products_raw = data["products"]
        products_dict = {}
        for product in products_raw:
            name = product["name"]
            price = float(product["price"])
            products_dict[name] = price
        return products_raw, products_dict, users

def save_products(product_list, users):
    with open("products.json", "w") as file:
        json.dump({"users": users, "products": product_list}, file, indent=2)

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

def print_receipt(summary):
    print("\n--- Receipt ---")
    print_receipt_rec(summary['order'], summary, 0)
    print("Thank you for shopping!\n")

def print_receipt_rec(order_items, summary, index):
    if index < len(order_items):
        item, qty = order_items[index]
        print(f"{item} x{qty} = {products[item] * qty:.2f}€")
        print_receipt_rec(order_items, summary, index + 1)
    else:
        print(f"Subtotal: {summary['subtotal']:.2f}€")
        print(f"Tax (19%): {summary['tax']:.2f}€")
        print(f"Total with tax: {summary['total_with_tax']:.2f}€")
        print(f"Discount: {summary['discount']:.2f}€")
        print(f"Discount percentage: {summary['discount_percentage']}")
        print(f"Final total: {summary['final']:.2f}€")

# --- Start Program ---

products_raw, products, users = load_products()

if login(retries=3):
    print("Starting the shopping program...\n")
    add_fake = input("Do you want to add fake products? (yes/no): ").strip().lower()
    if add_fake == "yes":
        clothes = generate_fake_clothes(10)
        for p in clothes:
            products[p["name"]] = float(p["price"])
        products_raw.extend(clothes)
        save_products(products_raw, users)
        print("✅ Fake products added.")
else:
    exit()

# Show products
print("Available products:")
for item in products_raw:
    print(f"{item['id']}. {item['name']}: {float(item['price']):.2f}€")
print()

order = []

while True:
    prod_id = input("Enter the ID of product: ").strip()
    selected = next((item for item in products_raw if item["id"] == prod_id), None)
    if selected:
        quant_input = input(f"Enter the quantity of {selected['name']}: ")
        if quant_input.isdigit():
            quant = int(quant_input)
            order.append((selected["name"], quant))
        else:
            print("Please enter a valid number.")
            continue
    else:
        print("Product ID not found.")
        continue

    add_more = input("Do you want to add more items? Enter 'yes' or 'no': ").strip().lower()
    if add_more != 'yes':
        break

summary = calculate_total_base(order, products)

def get_receipt_choice():
    while True:
        message = input("Do you want to print a receipt? (yes/no): ").strip().lower()
        if message in ("yes", "no"):
            return message
        else:
            print("Incorrect input! Please enter yes or no.")

receipt_choice = get_receipt_choice()
if receipt_choice == "yes":
    print_receipt(summary)
else:
    print("Goodbye!")
