from __future__ import print_function
from __future__ import division

from flask import Flask, request, render_template, jsonify, g
import sys
import json
import pickle
import drink

app = Flask(__name__)
app.json_encoder = drink.DrinkEncoder

class Settings :
    def __init__(self, ingredients, flow_rate ):
        self.ingredients = ingredients
        self.flow_rate = flow_rate

def open_files():
    """Opens the json file
    """
    if not hasattr(g, 'recipe_file'):
        g.recipe_file = open("recipes.json", "r")
    if not hasattr(g, 'settings_file'):
        try :
            g.settings_file = open("settings" ,"r")
        except IOError:
            f = open("settings", "w")
            f.close()
            g.settings_file = open('settings', "r")
    if not hasattr(g, 'ing_file'):
        g.ing_file = open('ingredients.json' , "r")

def close_files():
    if hasattr(g, 'recipe_file'):
        close(g.recipe_file)
        del g.recipe_file
    if hasattr(g,'settings_file'):
        close(g.settings_file)
        del g.settings_file
    if hasattr(g, ing_file):
        close(g.ing_file)
        del g.ing_file

def get_all_drinks():
    open_files()
    all_drinks = drink.read_drinks(g.recipe_file)
    return all_drinks

def get_all_ingredients():
    open_files()
    all_ingredients = drink.read_ingredients(g.ing_file)
    return all_ingredients

def start_drink(name):
    all_drinks = get_all_drinks()
    if name not in all_drinks :
        return False

    c_drink = all_drinks[name]
    ingredients = c_drink.ingredients
    all_ingredients = get_all_ingredients()
    pump_time = []
    flow_rate = get_flow_rate()
    for ing in ingredients :
        if ing.ingredient_name not in all_ingredients :
            print(ing.ingredient_name + " Error : returning .. ")
            return False
        pump_no = 0
        for g_i in all_ingredients :
            if ing.ingredient_name == g_i :
                break
            pump_no += 1
        pump_time.append(ing.amount/flow_rate)

    print(pump_time)
    start_progress()
    for i in range(len(pump_time)) :
        drink.enable_pump(i, pump_time[i])
    stop_progress()
    return True

def start_progress():
    print("Pumping started")

def stop_progress():
    print("Pumping stopped")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_drinks')
def get_drinks():
    """
    get the drinks possible with the current ingredients
    """
    all_drinks = get_all_drinks()
    c_ing = current_ingredients()
    possible_drinks = []

    for d in all_drinks:
        add_drink = True
        for ingredient in all_drinks[d].ingredients:
            if ingredient.ingredient_name not in c_ing:
                add_drink = False
        if add_drink:
            possible_drinks.append(all_drinks[d])

    possible_drinks.sort()
    return json.dumps(possible_drinks, cls=drink.DrinkEncoder)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/make_drink')
def make_drink():
    print (request.args.get('name'), file=sys.stderr)
    timestampId = request.args.get('timestamp')
    print(timestampId, file=sys.stderr)
    result = start_drink(request.args.get('name'))
    return jsonify(result=result)

@app.route('/all_ingredients')
def all_ingredients():
    open_files()
    return jsonify(ingredients=drink.read_ingredients(g.ing_file))


def current_ingredients():
    open_files()
    settings=read_settings(g.settings_file)
    return settings['ingredients']

def get_flow_rate():
    open_files()
    settings=read_settings(g.settings_file)
    return settings['flow_rate']

@app.route('/current_settings')
def current_settings():
    open_files()
    return jsonify(read_settings(g.settings_file))

@app.route('/save_settings', methods=['POST'])
def save_settings():
    ingredients = [];
    flow_rate = 0;
    print("save_settings");
    request_json = json.loads(request.data)
    print(request_json)
    ingredients.append(request_json['pump1'])
    ingredients.append(request_json['pump2'])
    ingredients.append(request_json['pump3'])
    ingredients.append(request_json['pump4'])
    ingredients.append(request_json['pump5'])
    flow_rate = request_json['flow_rate']
    settings = Settings(ingredients, flow_rate)
    write_settings(settings)

    return "saved"

def read_settings(settings_file):
    settings = json.load(settings_file)
    return settings

def write_settings(settings):
    with open('settings', 'w') as f:
        json.dump(settings.__dict__,f)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=81)
