# -*- coding: utf-8 -*-
import csv

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

from kivy.properties import StringProperty

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
    pass

def button_callback(instance, value):
    print("Button {} is now {}".format(instance.text, value))
    session.query(Ingredient).filter_by(name=instance.text).update({"in_stock": button_map(value)})
    session.commit()

class TestScroll(ScrollView):
    ing_type = StringProperty('')
    def __init__(self, ing_type, **kwargs):
        super(TestScroll, self).__init__(**kwargs)
        self.ing_type = ing_type
        all_ings = session.query(Ingredient).filter_by(type=ing_type).order_by(Ingredient.id)
        grid = GridLayout(size_hint_y=None, cols=1, padding=10, spacing = 10)
        grid.bind(minimum_height=grid.setter('height'))
        label = Label(text=ing_type)
        grid.add_widget(label)
        for ing in all_ings:
            button = ScrollButton(text=ing.name.encode('utf-8'), state=button_map(ing.in_stock))
            button.bind(state=button_callback)
            grid.add_widget(button)
        self.add_widget(grid)

# Declare both screens
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        box = BoxLayout(orientation='horizontal', padding=(10,40,10,10), spacing=10)
        with open('Ingredients.csv') as f:
            reader = csv.reader(f, delimiter=',')
            header = reader.next()
            for ing_type in header:
                scroll = TestScroll(ing_type, size_hint=(1,1), do_scroll_x=False)
                box.add_widget(scroll)
        self.add_widget(box)

class SettingsScreen(Screen):
    pass

class ScreenFake(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(ScreenFake(name='fake'))

class RecipeApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    RecipeApp().run()
