from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from telas import *

Window.size = (360, 640) # tamanho da janela do aplicativo

class HotReload(MDApp):
    KV_FILES = ['main.kv']
    DEBUG = True
    def build_app(self):
        return Builder.load_file('main.kv')
    
HotReload().run()