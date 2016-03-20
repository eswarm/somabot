from __future__ import print_function
from flask import Flask, request, render_template, jsonify
import sys
import json
import pickle
import drink as D 

app = Flask(__name__)

@app.route('/')
def index():
    f = open("drinks","r")
    drinks_json = json.loads(f.read())
    f = open("ingredients", "rb")
    ingredients_list = pickle.load(f)
    p = open("ingredients.json", "r")
    possible = json.loads(p.read())

    print(ingredients_list, file=sys.stderr)
    possible_ingredients = []
    
    for p in possible.keys():
        possible_ingredients.append(p)

    all_drinks = D.read_drinks("recipes.json")

    D.read_pump_mapping() 

    possible_drinks = []

    for drink in all_drinks:
        add_drink = True
        for ingredient in drink.ingredients:
            if (ingredient.ingredient_name not in ingredients_list):
                add_drink = False
        if (add_drink):
            possible_drinks.append(drink)
    #print (possible_drinks[0].name, file=sys.stderr)
    
    possible_drinks.sort(key=lambda x: x.name)
    #print (possible_ingredients, file=sys.stderr)
    possible_ingredients.sort()
    return render_template('index.html', possible_drinks = possible_drinks,
        ingredients_list = ingredients_list, possible_ingredients = possible_ingredients)

@app.route('/settings')
def settings():
    print ("IN SETTINGS", file=sys.stderr)
    ingredients = request.args.get('ingredients').split(",")
    print ("settings updated: ingredients = {ingredients}".format(ingredients=ingredients), file=sys.stderr)
    f = open("ingredients", "wb")
    pickle.dump(ingredients,f)
    return jsonify(result=0)

@app.route('/make_drink')
def make_drink():
    print (request.args.get('name'), file=sys.stderr)
    timestampId = request.args.get('timestamp')
    print(timestampId, file=sys.stderr)
    D.make_drink(request.args.get('name')) 
    return jsonify(result=0)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
