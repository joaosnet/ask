from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from botoes import *
from telas import *
from gpshelper import *
from gpsblinker import *
from pesquisa import *
from kivy_garden.mapview import MapView
from kivymd.uix.menu import MDDropdownMenu

class HotReload(MDApp):
    DEBUG = True
    KV_FILES = ['kv\mapage1.kv']
    def build_app(self, first=True):
        return Builder.load_file('kv\mapage1.kv')

if __name__ == '__main__':
    HotReload().run()