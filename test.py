from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget

class MainWidget(Widget):
    pass

class TestApp(App):
    def build(self):
        return MainWidget()

if __name__ == '__main__':
    TestApp().run()
