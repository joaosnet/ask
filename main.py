from kivymd.app import MDApp
from kivy.core.window import Window
from telas import *
from botoes import *

Window.size = (360, 800) # tamanho da janela do aplicativo

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Carregando arquivos kv
        self.load_all_kv_files(self.directory)
        # Gerenciador de Telas
        self.sm = MDScreenManager()

    def build(self):
        self.sm.add_widget(TutorialPage1(name='tutorialpage1'))
        self.sm.add_widget(TutorialPage2(name='tutorialpage2'))
        self.sm.add_widget(TutorialPage3(name='tutorialpage3'))
        self.sm.add_widget(StartPage(name='startpage'))
        self.sm.add_widget(HomePage(name='homepage'))
        self.sm.add_widget(PerfilPage(name='perfilpage'))
        self.sm.add_widget(LoadingPage(name='loadingpage'))
        self.sm.add_widget(MapaPage(name='mapapage'))
        self.sm.add_widget(CadastroPage(name='cadastropage'))
        self.sm.add_widget(LoginPage(name='loginpage'))
        return self.sm

    def mudar_tela(self, nome_tela):
        # print(id_tela)
        gerenciador_telas = self.sm
        gerenciador_telas.current = nome_tela
    
MainApp().run()