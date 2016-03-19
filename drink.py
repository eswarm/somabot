import json
from io_write import *

CL = "cl"
ML = "ml"
g_drinks = {}
#in ml per second
FLOW_RATE = 5
g_ingredients = []

class Ingredient:
    def __init__(self, unit, amount, ingredient_name):
        self.unit = unit
        self.amount = amount
        self.ingredient_name = ingredient_name

class Drink :
    def __init__(self, name, glass, category, ingredients):
        self.name = name
        self.glass = glass
        self.category = category
        self.ingredients = ingredients

def read_ingredients(in_location) :
    with open(in_location) as in_file:
        in_json = json.load(in_file)
        for key in in_json :
            print key + " " + str(in_json[key])

def read_drinks(json_location):
    drinks = {}
    all_drinks = []
    with open(json_location) as json_file:
        json_drinks = json.load(json_file)
        for json_drink in json_drinks :
            name = json_drink["name"]
            glass = json_drink.get("glass" , "any")
            category = json_drink.get("category" , "none")
            ingredients_json = json_drink["ingredients"]
            ingredients = []
            for ingredient in ingredients_json :
                if "special" in ingredient :
                    continue
                try :
                    unit = ingredient["unit"]
                    amount = ingredient["amount"]
                    ingredient_type = ingredient["ingredient"]
                    ingredients.append(Ingredient(unit,amount,ingredient_type))
                except :
                    print "Failed at " + name
            drinks[name] = Drink(name, glass, category, ingredients)
            all_drinks.append(drinks)
        print drinks[name]
    return all_drinks

def make_drink(name):
    Drink d = drink["name"]
    ingredients = d.ingredients
    pump_time = []
    for i in ingredients :
        pump_no = -1
        for g_i in g_ingredients :
            if ingredients.name == g_i :
                
            pump_no += 1
        if i.unit == CL :

"""
Read the list of pump mappings
"""
def read_pump_mapping():
    pkled_data = open("ingredients", "rb")
    pump_mapping = pickle.load(pkled_data)
    g_ingredients = pump_mapping
    # show error here


if __name__ == "__main__" :
    #read_ingredients("ingredients.json")
    read_drinks("recipes.json")
