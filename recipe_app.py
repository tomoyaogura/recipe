# -*- coding: utf-8 -*-
import csv

from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.properties import StringProperty, ObjectProperty

import fonts_ja
from database import session
from models import Ingredient, Recipe

Builder.load_file('/home/tommy/Hackathon/recipe/recipe.kv')
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

def button_map(state):
    if type(state) == bool:
        if state:
            return "down"
        else:
            return "normal"
    elif type(state) == str:
        return state == "down"

class ScrollButton(ToggleButton):
    def button_callback(self):
        print("Button {} is now {}".format(self.text, self.state))
        session.query(Ingredient).filter_by(name=self.text).update({"in_stock": button_map(self.state)})
        session.commit()

class TestScroll(ScrollView):
    ing_type = StringProperty('')
    grid = ObjectProperty()
    def __init__(self, ing_type, **kwargs):
        super(TestScroll, self).__init__(**kwargs)
        self.ing_type = ing_type

    def update(self):
        all_ings = session.query(Ingredient).filter_by(type=self.ing_type).order_by(Ingredient.id)
        label = Label(text=self.ing_type)
        self.grid.add_widget(label)
        for ing in all_ings:
            button = ScrollButton(text=ing.name.encode('utf-8'), state=button_map(ing.in_stock))
            self.grid.add_widget(button)

class IngredientScreen(Screen):
    ings_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(IngredientScreen, self).__init__(**kwargs)
        with open('Ingredients.csv') as f:
            reader = csv.reader(f, delimiter=',')
            header = reader.next()
            for ing_type in header:
                scroll = TestScroll(ing_type)
                self.ings_list.add_widget(scroll)

class MainScreen(Screen):

    pass

class RadioButtonSelector(Widget):
    pass

class RecipeScreen(Screen):
    pass
# Create the screen manager
#sm = ScreenManager()
#sm.add_widget(MenuScreen(sm, name='Ingredients'))
#sm.add_widget(SettingsScreen(sm, name='Recipe'))
#sm.add_widget(ScreenFake(sm, name='Shopping'))

class RecipeApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    RecipeApp().run()
