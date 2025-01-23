from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
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

        for num in self.sequence:
            button = Button(text=str(num), font_size=20, background_color=(0.2, 0.6, 1, 1))
            button.bind(on_press=self.on_button_press)
            self.buttons.append(button)
            self.root_layout.add_widget(button)

        return self.root_layout

    def on_button_press(self, instance):
        # ตรวจสอบว่าปุ่มที่กดเป็นลำดับตัวเลขที่ถูกต้องหรือไม่
        if int(instance.text) == self.current_index:
            instance.background_color = (0, 1, 0, 1)  # สีเขียวถ้ากดถูก
            instance.disabled = True  # ปิดการใช้งานปุ่มที่กดไปแล้ว
            self.current_index += 1  # ไปยังตัวเลขถัดไป
    
    def show_game_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Game Over! Congratulations!", font_size=20))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        content.add_widget(close_button)

        popup = Popup(title="Game Win!",
                      content=content,
                      size_hint=(0.6, 0.4),
                      auto_dismiss=False)

        close_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    SequenceGameApp().run()
