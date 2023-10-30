from kivymd.app import MDApp
from kivy.core.window import Window
from telas import *
from botoes import *
from myfirebase import MyFirebase
import requests
from pprint import pprint as pp

Window.size = (360, 800) # tamanho da janela do aplicativo

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Carregando arquivos kv
        self.load_all_kv_files(self.directory)
        # Gerenciador de Telas
        self.sm = MDScreenManager()
        self.firebase = MyFirebase()

    def build(self):
        self.sm.add_widget(TutorialPage1(name='tutorialpage1'))
        self.sm.add_widget(TutorialPage2(name='tutorialpage2'))
        self.sm.add_widget(TutorialPage3(name='tutorialpage3'))
        self.sm.add_widget(StartPage(name='startpage'))
        self.sm.add_widget(HomePage(name='homepage'))
        self.sm.add_widget(PerfilPage(name='perfilpage'))
        self.sm.add_widget(LoadingPage(name='loadingpage'))
        self.sm.add_widget(MapaPage(name='mapapage'))
        self.sm.add_widget(CadastroPage(name='cadastropage', id="cadastropage"))
        self.sm.add_widget(LoginPage(name='loginpage'))
        return self.sm
    
    def on_start(self):

        # carregar as informacoes do usuario
        self.carregar_info_usuario()

    def carregar_info_usuario(self):
        try:
            with open("refresh_token.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            # pegar informacoes do usuario
            link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()

            # # preencher foto de perfil
            # avatar = requisicao_dic["foto_de_perfil"]
            # self.avatar = avatar
            # foto_perfil = self.root.ids["foto_perfil"]
            # foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # # preencher o ID Unico
            # id_vendedor = requisicao_dic["id_vendedor"]
            # self.id_vendedor = id_vendedor
            # pagina_ajustes = self.root.ids["ajustespage"]
            # pagina_ajustes.ids["id_vendedor"].text = f'Seu ID Único: {id_vendedor}'

            # # preencher o total de vendas
            # total_vendas = float(requisicao_dic["total_vendas"])
            # self.total_vendas = total_vendas
            # homepage = self.root.ids["homepage"]
            # homepage.ids["label_total_vendas"].text = f"[color=#000000]Total de Vendas:[/color] [b]R${total_vendas:,.2f}[/b]"

            # Quando preenchidas as informacoes, mudar para a homepage
            self.mudar_tela("homepage")
        
        # se nao tiver o arquivo de refresh token ou ocorrer outro erro, mudar para a tela de login e mostrar a excecao se for o segundo acesso do usuario ao app
        except Exception as excecao:
            pp(excecao)
            self.mudar_tela("loginpage") 

    def mudar_tela(self, nome_tela):
        # print(id_tela)
        gerenciador_telas = self.root
        gerenciador_telas.current = nome_tela
    
MainApp().run()