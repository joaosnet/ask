from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (360, 800) # tamanho da janela do aplicativo

class HotReload(MDApp):
    KV_FILES = ['kv/loginpage.kv']
    DEBUG = True
    def build_app(self):
        return Builder.load_file('kv/loginpage.kv')

HotReload().run()
    
