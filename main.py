from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from random import shuffle

class SequenceGameApp(App):
    def build(self):
        # สร้าง Layout หลัก
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

        return self.root_layout

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
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f"Game Over! Time: {self.time_elapsed:.1f} seconds", font_size=20))
        close_button = Button(text="Close", size_hint=(1, 0.2))
        content.add_widget(close_button)

        popup = Popup(title="Game Over",
                      content=content,
                      size_hint=(0.6, 0.4),
                      auto_dismiss=False)

        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    SequenceGameApp().run()
