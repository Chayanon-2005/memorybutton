from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from random import shuffle

class SequenceGameApp(App):
    def build(self):
        #สร้าง layout
        self.root_layout = GridLayout(cols=5, spacing=10, padding=10)
        #สร้าง 30 ปุ่ม
        self.buttons = []
        self.sequence = list(range(1, 31)) 
        shuffle(self.sequence)  # สุ่มลำดับของปุ่ม
        self.current_index = 1 #โดยให้เริ่มจาก 1


if __name__ == "__main__":
    SequenceGameApp().run()
