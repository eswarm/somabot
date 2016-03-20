import json
from io_write import *

CL = "cl"
ML = "ml"
g_drinks = {}
#in ml per second
FLOW_RATE = 0.3
g_ingredients = []
last_drink = None
btn_thread1 = None
btn_thread2 = None
led_thread = None

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

def read_ingredients(in_location) :
    with open(in_location) as in_file:
        in_json = json.load(in_file)
        for key in in_json :
            print key + " " + str(in_json[key])


def read_drinks(json_location):
    global g_drinks
    g_drinks = {}
    all_drinks = []
    with open(json_location) as json_file:
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
            g_drinks[name] = d
            all_drinks.append(d)
        #print drinks[name]
    return all_drinks

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
    global g_ingredients
    pkled_data = open("ingredients", "rb")
    pump_mapping = pickle.load(pkled_data)
    g_ingredients = pump_mapping
    # show error here

"""
def listenButtons() :

    global btn_thread1
    global btn_thread2

    btn_thread1 = BtnWatchThread(1, "button1", GPIO_BTN1)
    btn_thread2 = BtnWatchThread(2, "button2", GPIO_BTN2)
"""

def start_progress() :
    global led_thread
    led_thread = LEDWatchThread()
    LEDOn = True
    led_thread.start()

def stop_progress() :
    LEDOn = False
