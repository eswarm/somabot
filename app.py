from __future__ import print_function
from flask import Flask, request, render_template, jsonify, g
import sys
import json
import pickle
import drink

app = Flask(__name__)

def open_files():
    """Opens the json file
    """
    if not hasattr(g, 'recipe_file'):
        g.recipe_file = open("recipes.json", "r")
    if not hasattr(g, 'settings_file'):
        try :
            g.settings_file = open("settings.pickle" ,"r")
        except IOError:
            f = open("settings.pickle", "wb")
            f.close()
            g.settings_file = open('settings.pickle', "r")
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

def get_drinks():
    """
    get the drinks possible with the current ingredients
    """
    all_drinks = get_all_drinks()

    for drink in all_drinks:
        add_drink = True
        for ingredient in drink.ingredients:
            if ingredient.ingredient_name not in current_ingredients:
                add_drink = False
        if add_drink:
            possible_drinks.append(drink)

    possible_drinks.sort(key=lambda x: x.name)
    #print (possible_ingredients, file=sys.stderr)
    #possible_ingredients.sort()
    return possible_drinks


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/make_drink')
def make_drink():
    print (request.args.get('name'), file=sys.stderr)
    timestampId = request.args.get('timestamp')
    print(timestampId, file=sys.stderr)
    drink.make_drink(request.args.get('name'))
    return jsonify(result=0)

@app.route('/all_ingredients')
def all_ingredients():
    open_files()
    return jsonify(ingredients=drink.read_ingredients(g.ing_file))

@app.route('/current_ingredients')
def current_ingredients():
    open_files()
    return jsonify(current_ingredients=drink.read_settings(g.settings_file)['ingredients'])

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
    settings = drink.Settings(ingredients, flow_rate)
    drink.write_settings(settings)

    return "saved"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
