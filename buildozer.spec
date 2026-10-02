from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.label = Label(
            text="مرحباً بك في التطبيق!",
            font_size='24sp',
            halign='center'
        )
        layout.add_widget(self.label)
        
        btn = Button(
            text="اضغط هنا",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1)
        )
        btn.bind(on_press=self.on_button_click)
        layout.add_widget(btn)
        
        return layout

    def on_button_click(self, instance):
        self.label.text = "تم الضغط على الزر بنجاح!"

if __name__ == '__main__':
    MainApp().run()