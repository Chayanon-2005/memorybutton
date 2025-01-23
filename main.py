from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from random import shuffle

class SequenceGameApp(App):
    def build(self):
        self.root_layout = GridLayout(cols=5, spacing=10, padding=10)   