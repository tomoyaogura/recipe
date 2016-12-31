from database import session
from models import Recipe, Ingredient

def can_make(recipe):
    if type(recipe) == str:
        recipe = session.query(Recipe).filter_by(name=recipe).first()
        if not recipe:
            print("Could not find recipe {}".format(recipe))
            return

    ingredient = int(recipe.ingredients, base=2)
    # If in stock, stock_binary && ingredients = ingredients
    return (ingredient == (ingredient & get_bin_stock()))

def list_available_recipes():
    available_recipe = []
    unavailable_recipe = []
    recipes = session.query(Recipe).all()
    for recipe in recipes:
        if can_make(recipe):
            available_recipe.append(recipe)
        else:
            unavailable_recipe.append(recipe)
    return available_recipe, unavailable_recipe

def find_best_ingredients(unavailable_recipe):
    stock = get_stock()
    missing_ingredients = 0
    # Hack to calculate missing ingredients
    out_of_stock = get_out_of_stock()

    for recipe in unavailable_recipe:
        missing_ingredients += int(recipe.ingredients[2:])

    missing = []
    for i in out_of_stock:
        recipe_count = int((missing_ingredients / 10**i.bit_offset) % 10)
        missing.append((i, recipe_count))
    return sorted(missing, key=lambda x: x[1], reverse=True)

def test():
    return find_best_ingredients(list_available_recipes()[1])
"""
Stock Methods
"""
def print_ingredients():
    for ingredient in session.query(Ingredient).all():
        print(ingredient.name)

def print_recipes():
    for ingredient in session.query(Recipe).all():
        print(ingredient.name)

def print_stock():
    for ingredient in get_stock():
        print(ingredient.name)

def add_stock(ingredient):
    change_stock(ingredient, True)

def remove_stock(ingredient):
    change_stock(ingredient, False)

def change_stock(ingredient, in_stock):
    ing = session.query(Ingredient).filter_by(name=ingredient).first()
    if not ing:
        print("Could not find ingredient {}".format(ingredient))
        return
    ing.in_stock = in_stock
    session.add(ing)
    session.commit()

def get_bin_stock():
    """ Retrun Binary Representation of current stock """
    return sum([2**i.bit_offset for i in get_stock()])

def get_stock():
    """ Return list of in-stock ingredient objects """
    return session.query(Ingredient).filter_by(in_stock=True).all()

def get_out_of_stock():
    """ Return list of in-stock ingredient objects """
    return session.query(Ingredient).filter_by(in_stock=False).all()
