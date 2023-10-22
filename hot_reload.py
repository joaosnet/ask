from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from telas import *
from botoes import *

Window.size = (360, 800) # tamanho da janela do aplicativo

class HotReload(MDApp):
    KV_FILES = ['main.kv']
    DEBUG = True
    def build_app(self):
        return Builder.load_file('main.kv')

    def on_start(self):
        pass
    
    def mudar_tela(self, id_tela):
        # print(id_tela)
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela
    
HotReload().run()