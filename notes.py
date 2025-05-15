
# receipt 
while True:
    message = input("do you want to print a receipt? ")
    if message == "yes":
        print("test") # here we add tht total order after we calcilate it, and the-
                      # products that user choses
        print("goodbey!")
        break
    elif message == "no":
        print("goodbey!")
        break
    else:
        print("incorrect input! please inter yes or no")
        continue
def discout(product, price, quantity):
    subtotal = product * price * quantity
    tax = subtotal * 0,19
    subtotal_with_tax = subtotal + tax

    if subtotal_with_tax >= 200:
        discount = subtotal_with_tax * 0.2

    elif subtotal_with_tax >= 100:        
        discount = subtotal_with_tax * 0.1 
 
    else:
        discount = 0

    final_price = subtotal_with_tax - discount





#cart
# cart = [] # adding products to a cart
# for items in cart:
#              [i] = 0

#              result = []
# for i, item in enumerate(banks[:5], start=1):
#     result.append([i, item])

# #print the receipt
# banks = ["bank1", "bank2", "bank3", "bank4", "bank5", "bank6", "bank7", "bank8", "bank9", "bank10"]

# for i, item in enumerate(banks[:5], start=1):
#         print(i, item)



#             prod_price = prod.value
#             print(f"prod_price")
# else: print(f"does not exit")
