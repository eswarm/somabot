from __future__ import print_function
from flask import Flask, request, render_template, jsonify
import sys
import json
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    f = open("drinks","r")
    drinks_json = json.loads(f.read())
    f = open("ingredients", "rb")
    ingredients_list = pickle.load(f)

    print(ingredients_list, file=sys.stderr)

    possible_ingredients = ["Apple Juice", "Vodka", "Orange Juice", "Gin", "Whisky", "Schnapps", "Rum", "Lemon Juice", "Tomato Juice"]

    possible_drinks = []

    for drink in drinks_json["drinks"]:
        add_drink = True
        for ingredient in drink["ingredients"]:
            if (ingredient not in ingredients_list):
                add_drink = False
        if (add_drink):
            possible_drinks.append(drink)

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
    return jsonify(result=0)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
