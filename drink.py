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
    g_drinks = {}
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
            g_drinks[name] = Drink(name, glass, category, ingredients)
            all_drinks.append(drinks)
        #print drinks[name]
    return all_drinks

def make_drink(name):
    drink = g_drinks["name"]
    ingredients = drink.ingredients
    pump_time = []
    for ing in ingredients :
        if ing not in g_ingredients :
            return False
        pump_no = 0
        for g_i in g_ingredients :
            if ing.name == g_i :
                break
            pump_no += 1
        ml = 0;
        if ing.unit == CL :
            ml = ing.amount * 10
        else :
            ml = ing.amount
        pump_time.append(ing.amount/FLOW_RATE)

    for i in range(len(pump_time)) :
        enable_pump(i, pump_time[i])

"""
Read the list of pump mappings
"""
def read_pump_mapping():
    pkled_data = open("ingredients", "rb")
    pump_mapping = pickle.load(pkled_data)
    g_ingredients = pump_mapping
    # show error here
