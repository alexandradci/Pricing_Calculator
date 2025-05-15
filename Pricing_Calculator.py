import json

# load products from a JSON file
def load_products():
    with open("products.json", "r") as prod_db:
        products_list = json.load(prod_db)
        products_dict = {}
        for product in products_list:
            for name, price in product.items():
                products_dict[name] = float(price)
        return products_dict

# load products
products = load_products()

# print available products
print("Available products:")
for name, price in products.items():
    print(f"- {name}: {price}€")
print()  # empty line for spacing

# save products
def save_products(products):
    with open("products.json", "w") as prod_db:
        json.dump(products, prod_db)

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
products = load_products()
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

# blah blah blah
