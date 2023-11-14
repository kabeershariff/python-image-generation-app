from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.imagelist import MDSmartTile
import subprocess
import threading
from kivy.clock import mainthread

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
    
    txt2img_generate = ObjectProperty()
    img2img_generate = ObjectProperty()

    @mainthread
    def start_txt2img(self):
        steps = int(self.slider_steps_txt2img.value)
        cfg = int(self.slider_cfg_txt2img.value)
        amount = int(self.slider_amount_txt2img.value)
        prompt = self.txt2img_prompt.text
        remove = self.txt2img_negative_prompt.text

        script_name = "img_generate.py"
        script_args = ['--prompt', f'"{prompt}"','--remove', f'{remove}', '--amount', f'{amount}', '--steps', f'{steps}', '--cfg', f'{cfg}']
        self.disable_widgets()
        background_thread = threading.Thread(target=MainFunctions().command(script_name, script_args)).start()

    @mainthread
    def start_img2img(self):
        steps = int(self.slider_steps_img2img.value)
        cfg = int(self.slider_cfg_img2img.value)
        denoise = self.slider_denoise_img2img.value
        amount = int(self.slider_amount_img2img.value)
        prompt = self.img2img_prompt.text
        remove = self.img2img_negative_prompt.text
        image = self.img2img_path.text

        script_name = "img2img_generate.py"
        script_args = ['--prompt',f'"{prompt}"', '--remove', f'"{remove}', '--image', f'{image}', '--amount', f'{amount}', '--steps', f'{steps}', '--cfg', f'{cfg}', '--denoise', f'{denoise}']
        background_thread = threading.Thread(target=MainFunctions().command(script_name, script_args)).start()
    
    def load_images():
        pass

    def clear_images():
        pass

    @mainthread
    def enable_widgets(self):
        self.txt2img_generate.disabled = False
        self.img2img_generate.disabled = False

    @mainthread
    def disable_widgets(self):
        self.txt2img_generate.disabled = True
        self.img2img_generate.disabled = True

class MainFunctions:
    def command(self, script, script_arguments):
        print("running command")
        subprocess.call(['python', script] + script_arguments)
        MainScreen().enable_widgets()

class user_interfaceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Red"
        return MainScreen()

user_interfaceApp().run()
