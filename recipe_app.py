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
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel

from kivy.properties import StringProperty, ObjectProperty

import fonts_ja
from database import session
from models import Ingredient, Recipe

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

"""
MainMenu
- RecipeMenu
  - Accordian
    - Filter
    - RecipeSplitter
      - ScrollView
      - Menu
- IngredientMenu
- ShoppingMenu

"""


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

class CheckButton(CheckBox):
    pass

class TestScroll(ScrollView):
    def __init__(self, ing_type, is_button, **kwargs):
        super(TestScroll, self).__init__(**kwargs)
        layout = GridLayout(size_hint_y=None, cols=1, padding=10, spacing=10)
        layout.bind(minimum_height=layout.setter('height'))
        all_ings = session.query(Ingredient).filter_by(type=ing_type).order_by(Ingredient.id)
        label = Label(text=ing_type)
        layout.add_widget(label)
        for ing in all_ings:
            if is_button:
                button = ScrollButton(text=ing.name.encode('utf-8'), state=button_map(ing.in_stock))
            else:
                button = CheckButton(text=ing.name.encode('utf-8'))
            layout.add_widget(button)
        self.add_widget(layout)

class IngredientScreen(Screen):
    ings_list = ObjectProperty()
    def update(self):
        with open('Ingredients.csv') as f:
            reader = csv.reader(f, delimiter=',')
            header = reader.next()
            for ing_type in header:
                scroll = TestScroll(ing_type, True)
                self.ings_list.add_widget(scroll)

class RadioButtonSelector(Widget):
    pass

class MainScreen(Screen):
    ing_screen = ObjectProperty()
    rep_screen = ObjectProperty()

    def update(self):
        self.ing_screen.update()
        self.rep_screen.update()
    pass

class RecipeScreen(Screen):
    ings_list = ObjectProperty()
    scrolls = []
    selected_recipe = StringProperty("")
    def update(self):
        with open('Ingredients.csv') as f:
            reader = csv.reader(f, delimiter=',')
            header = reader.next()
            for ing_type in header:
                scroll = FilterScroll(ing_type)
                self.scrolls.append(scroll)
                self.ings_list.add_widget(scroll)
    def update_text(self, new_text):
        self.selected_recipe = session.query(Recipe).filter_by(name=new_text).first().__str__()
        return

class RecipeTreeLabel(TreeViewLabel):

    def clicked(self, obj, value):
        # For some reason... root does not work. We need to traverse tree
        self.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.update_text(self.text)

class RecipeScroll(ScrollView):
    tv = None
    def __init__(self, **kwargs):
        super(RecipeScroll, self).__init__(**kwargs)
        self.tv = TreeView(size_hint_y=None)
        self.update_tree()
        self.add_widget(self.tv)
        self.tv.bind(minimum_height=self.tv.setter('height'))

    def update_tree(self):
        types = set([r.type for r in session.query(Recipe).all()])
        for t in types:
            n1 = self.tv.add_node(TreeViewLabel(text=t))
            recipes = session.query(Recipe).filter_by(type=t).all()
            for r in recipes:
                r_node = RecipeTreeLabel(text=r.name)
                r_node.bind(is_selected=r_node.clicked)
                self.tv.add_node(r_node, n1)


class FilterScroll(ScrollView):
    buttons = []
    def __init__(self, ing_type, **kwargs):
        super(FilterScroll, self).__init__(**kwargs)
        layout = GridLayout(size_hint_y=None, cols=2, padding=10, spacing=10)
        layout.bind(minimum_height=layout.setter('height'))
        all_ings = session.query(Ingredient).filter_by(type=ing_type).order_by(Ingredient.id)
        for ing in all_ings:
            label = Label(text=ing.name.encode('utf-8'))
            button = CheckButton(name=ing.name.encode('utf-8'))
            self.buttons.append(button)
            layout.add_widget(label)
            layout.add_widget(button)
        self.add_widget(layout)

class RecipeApp(App):
    def build(self):
        ms = MainScreen()
        ms.update()
        return ms 

if __name__ == '__main__':
    RecipeApp().run()
