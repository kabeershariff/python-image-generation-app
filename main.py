from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.imagelist import MDSmartTile

class MainScreen(Screen):
    slider_steps_txt2img = ObjectProperty()
    slider_cfg_txt2img = ObjectProperty()
    slider_amount_txt2img = ObjectProperty()

    slider_steps_img2img = ObjectProperty()
    slider_cfg_img2img = ObjectProperty()
    slider_denoise_img2img = ObjectProperty()
    slider_amount_img2img = ObjectProperty()

    txt2img_prompt = ObjectProperty()
    txt2img_negative_prompt = ObjectProperty()

    img2img_prompt = ObjectProperty()
    img2img_negative_prompt = ObjectProperty()
    img2img_path = ObjectProperty()

    def start_txt2img():
        pass

    def start_img2img():
        pass
    
    def load_images():
        pass

    def clear_images():
        pass

class user_interfaceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Red"
        return MainScreen()

user_interfaceApp().run()
