from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from botoes import *
from telas import *
from kivy_garden.mapview import MapView
from kivymd.uix.menu import MDDropdownMenu

Window.size = (360, 800) # tamanho da janela do aplicativo


class HotReload(MDApp):
    KV_FILES = ['kv/perfilpage.kv']
    DEBUG = True
    def build_app(self):
        return Builder.load_file('kv/perfilpage.kv')

if __name__ == '__main__':
    HotReload().run()
    
