import json

products = {} # to change

with open("products.json", "w") as json_file: # to write a function that saves
    json.dump(products, json_file)

products["jeans"]={}

with open("products.json", "w") as json_file:
    json.dump(products, json_file)





# add items in your cart

# view cart

# apply discount


# The user inputs what the customer bought (product name + quantity).
# The program:
# Looks up the price in the JSON,
# Calculates subtotal,
# Applies discount,
# Adds tax,
# Prints a summary invoice

