import json, pickle
TEST_MODE = True

if TEST_MODE :
    def enable_pump(pump_no, time_interval) :
        print " pump " + str(pump_no) + " time " + str(time_interval)
else :
    from io_write import *

CL = "cl"
ML = "ml"
FLOW_RATE = 0.3


class Ingredient:
    def __init__(self, unit, amount, ingredient_name):
        self.unit = unit
        self.amount = amount
        self.ingredient_name = ingredient_name

class Drink :
    def __init__(self, name, glass, category, ingredients, preparation):
        self.name = name
        self.glass = glass
        self.category = category
        self.ingredients = ingredients
        self.preparation = preparation

class Settings :
    def __init__(self, ingredients, flow_rate ):
        self.ingredients = ingredients
        self.flow_rate = flow_rate

def read_settings(settings_file):
    settings = pickle.load(settings_file)
    return settings

def write_settings(settings):
    with open('settings.pickle', 'wb') as f:
        pickle.dump(settings, f)

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
                ingredient_type = ingredient["ingredient"]
                ingredients.append(Ingredient(unit,amount,ingredient_type))
            except :
                print "Failed at " + name
        d = Drink(name, glass, category, ingredients, preparation)
        drinks[name] = d
    #print drinks[name]
    return drinks

def make_drink(name):
    print g_drinks.keys()
    drink = g_drinks[name]
    ingredients = drink.ingredients
    pump_time = []
    print g_ingredients
    for ing in ingredients :
        if ing.ingredient_name not in g_ingredients :
            print
            print ing.ingredient_name + " Error : returning .. "
            return False
        pump_no = 0
        for g_i in g_ingredients :
            if ing.ingredient_name == g_i :
                break
            pump_no += 1
        ml = 0;
        if ing.unit == CL :
            ml = ing.amount * 10
        else :
            ml = ing.amount
        pump_time.append(ing.amount/FLOW_RATE)

    print pump_time
    start_progress()
    for i in range(len(pump_time)) :
        enable_pump(i, pump_time[i])
    stop_progress()

"""
Read the list of pump mappings
"""
def read_pump_mapping():
    #global g_ingredients
    pkled_data = open("ingredients", "rb")
    pump_mapping = pickle.load(pkled_data)
    g_ingredients = pump_mapping
    # show error here
