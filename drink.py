import json, time 
from json import JSONEncoder

TEST_MODE = True

if TEST_MODE :
    def enable_pump(pump_no, time_interval) :
        print " pump " + str(pump_no) + " time " + str(time_interval)
        time.sleep(time_interval)
else :
    from io_write import *

CL = "cl"
ML = "ml"

class DrinkEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Ingredient:
    def __init__(self, amount, ingredient_name):
        self.amount = amount
        self.ingredient_name = ingredient_name

class Drink :
    def __init__(self, name, glass, category, ingredients, preparation):
        self.name = name
        self.glass = glass
        self.category = category
        self.ingredients = ingredients
        self.preparation = preparation

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)


def read_ingredients(ing_file):
    ing = json.load(ing_file)
    ingredients = ing.keys()
    ingredients.sort()
    return ingredients

def read_drinks(json_file):
    drinks = {}
    json_drinks = json.load(json_file)
    for json_drink in json_drinks :
        name = json_drink["name"]
        glass = json_drink.get("glass" , "any")
        category = json_drink.get("category" , "none")
        ingredients_json = json_drink["ingredients"]
        preparation = json_drink.get("preparation", "No preparation")
        ingredients = []
        for ingredient in ingredients_json :
            if "special" in ingredient :
                continue
            try :
                unit = ingredient["unit"]
                amount = ingredient["amount"]
                if unit == CL :
                    amount = amount * 10
                ingredient_type = ingredient["ingredient"]
                ingredients.append(Ingredient(amount,ingredient_type))
            except :
                print "Failed at " + name
        d = Drink(name, glass, category, ingredients, preparation)
        drinks[name] = d
    #print drinks[name]
    return drinks

"""
Read the list of pump mappings
"""
def read_pump_mapping():
    #global g_ingredients
    pkled_data = open("ingredients", "rb")
    pump_mapping = pickle.load(pkled_data)
    g_ingredients = pump_mapping
    # show error here
