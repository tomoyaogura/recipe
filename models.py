# -*- coding: utf-8 -*-
import enum
import csv

from database import Base, session, engine
from sqlalchemy import Column, Integer, String, Binary, Text, PickleType, Boolean

class Difficulty(enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class Type(enum.Enum):
    main = "Main"
    side = "Side"
    dessert = "Dessert"

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    difficulty = Column(String())
    # Bitmap of Current resources. 
    # Recipe can be made IF ingred & recipe == recipe
    ingredients = Column(Binary())
    optional_ingredients = Column(Binary())
    ingredients_text = Column(Text())
    seasoning = Column(Text())
    portion = Column(Text())
    directions = Column(Text())
    notes = Column(Text())
    type = Column(Text())

    def __init__(self, name, difficulty, type, ingredients, ingredients_text, directions, seasoning="", portion="", notes="", optional_ingredients=bin(0)):
        self.name = name
        self.difficulty = difficulty
        self.ingredients = ingredients
        self.optional_ingredients = optional_ingredients
        self.ingredients_text = ingredients_text
        self.directions = directions
        self.seasoning = seasoning
        self.portion = portion
        self.notes = notes
        self.type = type

    def __str__(self):
        string = self.name.encode('utf-8') + "\n"
        string += self.portion.encode('utf-8') + "\n"
        string += self.ingredients_text.encode('utf-8') + "\n\n"
        string += self.directions.encode('utf-8') + "\n"
        string += self.notes.encode('utf-8')
        return string

    def list_ingredients(self):
        binary = int(self.ingredients, base=2)
        ingredients = []
        ings = session.query(Ingredient).all()
        for ing in ings:
            index = ing.bit_offset
            if(2**index == (2**index & binary)):
                ingredients.append(ing)
        return ingredients

    def list_optional_ingredients(self):
        binary = int(self.optional_ingredients, base=2)
        ingredients = []
        ings = session.query(Ingredient).all()
        for ing in ings:
            index = ing.bit_offset
            if(2**index == (2**index & binary)):
                ingredients.append(ing)
        return ingredients


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    bit_offset = Column(Integer())
    stores = Column(PickleType())
    on_shopping_list = Column(Boolean())
    in_stock = Column(Boolean())
    type = Column(String())

    def __init__(self, name, bit_offset, type, stores=None):
        self.name = name
        self.bit_offset = bit_offset
        self.stores = stores
        self.on_shopping_list = False
        self.in_stock = False
        self.type = type

    def get_bit_mask(self):
        return 2**self.bit_offset

"""
METHOD TO SET DATABASE
"""
def init_models():
    if True:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Initializing Tables Done")

    if True:
        print("Reading Ingredients.txt for ingredients")    
        with open('recipes/Ingredients.csv') as f:
            ing_id = 0
            reader = csv.reader(f, delimiter=',')
            header = reader.next()
            for row in reader:
                for i in range(len(row)):
                    if row[i]:
                        ing = Ingredient(name=row[i], type=header[i], bit_offset=ing_id)
                        ing_id += 1
                        session.add(ing)
            session.commit()

    if True:
        print("Reading Recipe.csv for recipes") 
        with open('recipes/Recipes.csv') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                name = row[0]
                print name
                type = row[1]
                difficulty = row[2]
                instructions = row[3]
                all_ingredients = row[4:]
                optional_ingredients = [i.decode("utf-8")[1:] for i in all_ingredients if i and i.decode("utf-8")[0] == u"＊"]
                ingredients = [i for i in all_ingredients if i and i.decode("utf-8")[0] != u"＊"]
                ing_models = session.query(Ingredient).filter(Ingredient.name.in_(ingredients)).all()
                opt_ing_models = session.query(Ingredient).filter(Ingredient.name.in_(optional_ingredients)).all()
                bin_val = sum([2**i.bit_offset for i in ing_models])
                bin_val = bin(bin_val)
                opt_bin_val = sum([2**i.bit_offset for i in opt_ing_models])
                opt_bin_val = bin(opt_bin_val)
                ingredients_text = [i for i in all_ingredients if i]
                recipe = Recipe(name, difficulty, type, bin_val, "\n".join(ingredients_text), instructions, optional_ingredients=opt_bin_val)
                session.add(recipe)
            session.commit()

    if True:
        print("Reading Recipe.txt for Recipes") 
    print("Finished importing Ingredients and Recipes")

if __name__=="__main__":
    init_models()
