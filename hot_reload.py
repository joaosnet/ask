from kaki.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from botoes import *
from telas import *
from gpshelper import GpsHelper
from gpsblinker import GpsBlinker
from pesquisa import Search_Select_Option, SearchTextInput
from kivy_garden.mapview import MapView
from kivymd.uix.menu import MDDropdownMenu
import os

class HotReload(App, MDApp):
    DEBUG = True
    AUTORELOADER_PATHS = [
        (os.getcwd(), {'recursive': True}),
    ]
    def build_app(self):
        return Builder.load_file('kv\mapage1.kv')
    
if __name__ == '__main__':
    HotReload().run()