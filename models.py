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
    directions = Column(Text())
    notes = Column(Text())

    def __init__(self, name, difficulty, ingredients, directions, notes):
        self.name = name
        self.difficulty = difficulty
        self.ingredients = ingredients
        self.directions = directions
        self.notes = notes

    def list_ingredients(self):
        binary = int(self.ingredients, base=2)
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

    def __init__(self, name, bit_offset, stores=None):
        self.name = name
        self.bit_offset = bit_offset
        self.stores = stores
        self.on_shopping_list = False
        self.in_stock = False 
        self.type = "N/A"

"""
METHOD TO SET DATABASE
"""
def init_models():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Initializing Tables Done")
    print("Reading Ingredients.txt for ingredients")    
    with open('Ingredients.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            ing = Ingredient(name=row[0], bit_offset=row[1])
            session.add(ing)
        session.commit()
    print("Reading Recipe.txt for recipes") 
    with open('Recipes.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            name = row[0]
            difficulty = row[1]
            instructions = row[2]
            ingredients = row[3:]
            ing_models = session.query(Ingredient).filter(Ingredient.name.in_(ingredients)).all()
            bin_val = sum([2**i.bit_offset for i in ing_models])
            bin_val = bin(bin_val)
            recipe = Recipe(name, difficulty, bin_val, instructions, "")
            session.add(recipe)
        session.commit()
    print("Finished importing Ingredients and Recipes")

