from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from botoes import *
from telas import *
from gpshelper import *
from kivy_garden.mapview import MapView
from kivymd.uix.menu import MDDropdownMenu


class HotReload(MDApp):
    DEBUG = True
    def build_app(self):
        return Builder.load_file('kv\mapage2.kv')

if __name__ == '__main__':
    HotReload().run()
    
