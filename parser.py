# -*- coding: utf-8 -*-
import csv
from models import Recipe, Ingredient
from database import session

MAPPER = {0: "Name",
          1: "Portion",
          2: "Difficulty",
          3: "Type",
          4: "Ingredients",
          5: "Seasoning",
          6: "Directions",
          7: "Notes"}

INGREDIENT = {"Name": "",
              "Ingredients": "",
              "Seasoning": "",
              "Directions": "",
              "Notes": ""}

# PARSING JAPANESE IS WERID. 
def parse_ingredient_dict(ing_dict):
    japanese_space = "　"
    ingredients = [line.split(japanese_space) for line in ing_dict[4].splitlines()]
    #seasoning = [line.split(japanese_space) for line in ing_dict[4].splitlines()]
    directions = ing_dict[5]
    notes = ing_dict[6]
    ingredient_bit = 0
    all_ingredients = []
    opt_ingredient_bit = 0
    for ingredient in ingredients:
        if ingredient[0][0] == "*":
            print("{} is optional... skipping".format(ingredient[0]))
            ing_model = session.query(Ingredient).filter_by(name=ingredient[0].decode('utf-8')[1:]).first()
            if ing_model:
                opt_ingredient_bit += ing_model.get_bit_mask()
            continue
        ing_model = session.query(Ingredient).filter_by(name=ingredient[0]).first()
        all_ingredients.append(ingredient[0])
        if not ing_model:
            print("Could not find {}".format(ingredient[0]))
        else:
            ingredient_bit += ing_model.get_bit_mask()
    with open('recipe_text.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        lists = [ing_dict[0], ing_dict[2], ing_dict[3], ing_dict[6]]
        lists = lists + all_ingredients
        writer.writerow(lists)
    rec = Recipe(name=ing_dict[0],
                 type=ing_dict[3],
                 difficulty=ing_dict[2],
                 ingredients=bin(ingredient_bit),
                 optional_ingredients=bin(opt_ingredient_bit),
                 ingredients_text=ing_dict[4],
                 directions=ing_dict[6],
                 notes=ing_dict[7],
                 seasoning=ing_dict[5],
                 portion=ing_dict[1])
    session.add(rec)
    session.commit()

def read_file():
    with open("Recipe.txt") as text:
        index = 0
        recipe = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: ""}
        for line in text:
            # Start of new section
            if(line[0] == "-"):
                index += 1
            # End of Section
            elif(line[0] == "="):
                index = 0
                parse_ingredient_dict(recipe)
                for i in recipe.keys():
                    recipe[i] = ""
            else:
                if (index >= 0 and index <= 3):
                    recipe[index] = line
                elif (index == 4):
                    recipe[4] += line
                elif (index == 5):
                    # Direction
                    if(line[0].isdigit()):
                        recipe[6] += line
                    # If Seasoning
                    else:
                        recipe[5] += line
                # Direction
                elif (index == 6):
                    recipe[6] += line
                elif (index == 7):
                    recipe[7] += line
if __name__ == "__main__":
    read_file()
