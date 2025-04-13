import json

products = {} # to change

with open("products.json", "w") as json_file: # to write a function that saves
    json.dump(products, json_file)

products["jeans"]={}

# for employee in employees:
    #  for key, value in employee.items():
        #   print(f"{key} is a {value}")
# 

with open("products.json", "w") as json_file:
    json.dump(products, json_file)




