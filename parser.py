# -*- coding: utf-8 -*-
import csv
from models import Recipe, Ingredient
from database import session

MAPPER = {0: "Name",
          1: "Portion",
          2: "Difficulty",
          3: "Ingredients",
          : "Seasoning",
          5: "Directions",
          6: "Notes"}

INGREDIENT = {"Name": "",
              "Ingredients": "",
              "Seasoning": "",
              "Directions": "",
              "Notes": ""}

# PARSING JAPANESE IS WERID. 
def parse_ingredient_dict(ing_dict):
    japanese_space = "　"
    ingredients = [line.split(japanese_space) for line in ing_dict[3].splitlines()]
    #seasoning = [line.split(japanese_space) for line in ing_dict[4].splitlines()]
    directions = ing_dict[5]
    notes = ing_dict[6]
    ingredient_bit = 0
    all_ingredients = []
    for ingredient in ingredients:
        if ingredient[0][0] == "*":
            print("{} is optional... skipping".format(ingredient[0]))
            continue
        ing_model = session.query(Ingredient).filter_by(name=ingredient[0]).first()
        all_ingredients.append(ingredient[0])
        if not ing_model:
            print("Could not find {}".format(ingredient[0]))
        else:
            ingredient_bit += ing_model.get_bit_mask()
    with open('recipe_text.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        lists = [ing_dict[0], ing_dict[2], ing_dict[5]]
        lists = lists + all_ingredients
        writer.writerow(lists)
    rec = Recipe(name=ing_dict[0],
                 type="FALSE",
                 difficulty=ing_dict[2],
                 ingredients=bin(ingredient_bit),
                 ingredients_text=ing_dict[3],
                 directions=ing_dict[5],
                 notes=ing_dict[6],
                 seasoning=ing_dict[4],
                 portion=ing_dict[1])
    session.add(rec)
    session.commit()

def read_file():
    with open("Recipe.txt") as text:
        index = 0
        recipe = {0: "", 1: "", 2: "", 3: "", 4: "", 5: "", 6: ""}
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
                if (index == 0):
                    recipe[0] = line
                elif (index == 1):
                    recipe[1] = line
                elif (index == 2):
                    recipe[2] = line
                elif (index == 3):
                    recipe[3] += line
                elif (index == 4):
                    # Direction
                    if(line[0].isdigit()):
                        recipe[5] += line
                    # If Seasoning
                    else:
                        recipe[4] += line
                # Direction
                elif (index == 5):
                    recipe[5] += line
                elif (index == 6):
                    recipe[6] += line
if __name__ == "__main__":
    read_file()
