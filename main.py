from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from telas import *

Window.size = (360, 640) # tamanho da janela do aplicativo
class MainApp(MDApp): # classe principal do aplicativo

    def build(self): # metodo que constroi o aplicativo
        return Builder.load_file('main.kv') # conecta o arquivo main.kv com o main.py


MainApp().run() # roda o aplicativo