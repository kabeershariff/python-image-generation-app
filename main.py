from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class MainScreen(Screen):
    def demo():
        pass

class user_interfaceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Red"
        return MainScreen()

user_interfaceApp().run()
