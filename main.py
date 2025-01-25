from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from random import shuffle

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # เพิ่มรูปภาพในหน้าจอเริ่มเกม
        image = Image(source='start_screen.png', size_hint=(1, 0.6))
        start_label = Label(text="Welcome to the Sequence Game!", font_size=24, size_hint=(1, 0.2))
        start_button = Button(text="Start Game", font_size=20, size_hint=(1, 0.2))
        start_button.bind(on_press=self.start_game)

        layout.add_widget(image)
        layout.add_widget(start_label)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "game"

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None  # เก็บ reference ของ Popup เพื่อจัดการ
        self.root_layout = GridLayout(cols=5, spacing=10, padding=10)

        # สร้างปุ่ม 30 ปุ่ม
        self.buttons = []
        self.sequence = list(range(1, 31))  # ลำดับตัวเลขที่ต้องกด
        shuffle(self.sequence)  # สุ่มลำดับของปุ่ม
        self.current_index = 1  # เริ่มจากตัวเลข 1

        for num in self.sequence:
            button = Button(text=str(num), font_size=20, background_color=(0.2, 0.6, 1, 1))
            button.bind(on_press=self.on_button_press)
            self.buttons.append(button)
            self.root_layout.add_widget(button)

        # ตั้งค่าตัวจับเวลา
        self.time_elapsed = 0
        self.timer_label = Label(text="Time: 0.0 seconds", font_size=20, size_hint=(1, 0.1))
        self.root_layout.add_widget(self.timer_label)

        # เริ่มจับเวลา
        self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)

        self.add_widget(self.root_layout)

    def update_timer(self, dt):
        # อัปเดตเวลาที่ผ่านไป
        self.time_elapsed += dt
        self.timer_label.text = f"Time: {self.time_elapsed:.1f} seconds"

    def on_button_press(self, instance):
        # ตรวจสอบว่าปุ่มที่กดเป็นลำดับตัวเลขที่ถูกต้องหรือไม่
        if int(instance.text) == self.current_index:
            instance.background_color = (0, 1, 0, 1)  # สีเขียวถ้ากดถูก
            instance.disabled = True  # ปิดการใช้งานปุ่มที่กดไปแล้ว
            self.current_index += 1  # ไปยังตัวเลขถัดไป

            if self.current_index > len(self.sequence):
                self.end_game()
        else:
            # เพิ่มเวลาเมื่อกดผิดปุ่ม
            self.time_elapsed += 2  # เพิ่มเวลา 2 วินาที
            self.flash_red(instance)  # ทำให้ปุ่มกระพริบสีแดง

    def flash_red(self, instance):
        # ทำให้ปุ่มกระพริบสีแดง
        def restore_color(dt):
            instance.background_color = (0.2, 0.6, 1, 1)  # คืนสีเดิมหลังจากกระพริบ
        instance.background_color = (1, 0, 0, 1)  # เปลี่ยนสีปุ่มเป็นสีแดง
        Clock.schedule_once(restore_color, 0.5)  # เปลี่ยนกลับหลัง 0.5 วินาที

    def end_game(self):
        # จบเกมและหยุดจับเวลา
        self.timer_event.cancel()
        self.show_game_popup()

    def show_game_popup(self):
        # สร้าง Popup แสดงข้อความจบเกม
        if self.popup:  # หากมี Popup เปิดอยู่ ให้ปิดก่อน
            self.popup.dismiss()

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Game Over! Time: {self.time_elapsed:.1f} seconds", font_size=20))

        restart_button = Button(text="Restart Game", size_hint=(1, 0.2))
        close_button = Button(text="Close", size_hint=(1, 0.2))

        content.add_widget(restart_button)
        content.add_widget(close_button)

        self.popup = Popup(title="Game Over",
                           content=content,
                           size_hint=(0.6, 0.4),
                           auto_dismiss=False)

        restart_button.bind(on_press=self.restart_game)
        close_button.bind(on_press=self.close_popup)
        self.popup.open()

    def restart_game(self, instance):
        # รีเซ็ตสถานะเกมและเริ่มเกมใหม่
        if self.popup:
            self.popup.dismiss()
        self.manager.current = "start"
        self.manager.get_screen("game").reset_game()

    def close_popup(self, instance):
        if self.popup:
            self.popup.dismiss()

    def reset_game(self):
        # รีเซ็ตเกม
        self.root_layout.clear_widgets()
        self.__init__()

class SequenceGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == "__main__":
    SequenceGameApp().run()
