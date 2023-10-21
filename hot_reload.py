from kivymd.tools.hotreload.app import MDApp
from kivy.lang import Builder

class HotReload(MDApp):
    KV_FILES = ['kv/inclusiveway.kv']
    DEBUG = True
    def build_app(self):
        return Builder.load_file('kv/inclusiveway.kv')
    
HotReload().run()