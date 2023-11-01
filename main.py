from kivymd.app import MDApp
from kivy.core.window import Window
from telas import *
from botoes import *
from myfirebase import MyFirebase
import requests
from pprint import pprint as pp
import traceback

Window.size = (360, 800) # tamanho da janela do aplicativo

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Carregando arquivos kv
        self.load_all_kv_files(self.directory)
        # Gerenciador de Telas
        self.sm = MDScreenManager()
        self.firebase = MyFirebase()
        self.visitas_app = 0

    def build(self):
        self.sm.add_widget(TutorialPage1(name='tutorialpage1'))
        self.sm.add_widget(TutorialPage2(name='tutorialpage2'))
        self.sm.add_widget(TutorialPage3(name='tutorialpage3'))
        self.sm.add_widget(StartPage(name='startpage'))
        self.sm.add_widget(HomePage(name='homepage', id="homepage"))
        # self.sm.add_widget(PerfilPage(name='perfilpage'))
        self.sm.add_widget(LoadingPage(name='loadingpage'))
        self.sm.add_widget(MapaPage(name='mapapage'))
        self.sm.add_widget(CadastroPage(name='cadastropage', id="cadastropage"))
        self.sm.add_widget(LoginPage(name='loginpage'))
        return self.sm
    
    def on_start(self):
        # self.visitas_app += 1
        # carregar as informacoes do usuario
        self.carregar_info_usuario()

    def carregar_info_usuario(self):
        try:
            try:
                # carrengado o email e senha do arquivo usuario.txt
                with open("usuario.txt", "r") as arquivo:
                    email, senha = arquivo.read().splitlines()
                # escrevendo nos campos de email e senha
                pagina_login = self.root.get_screen("loginpage")
                pagina_login.ids["email"].text = email
                pagina_login.ids["senha"].ids["text_field"].text = senha
                pagina_login.ids["caixa_selecao"].active = True
            except Exception as excecao:
                print("Deu um erro ao carregar o email e senha do arquivo usuario.txt:", excecao)
                traceback.print_exc()

            with open("refresh_token.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token
            # pegar informacoes do usuario
            link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()
            # pp(requisicao_dic)

            # # preencher foto de perfil
            # avatar = requisicao_dic["foto_de_perfil"]
            # self.avatar = avatar
            # foto_perfil = self.root.ids["foto_perfil"]
            # foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher o ID Unico do usuario
            id = requisicao_dic["id"]
            self.id = id
            self.root.get_screen("homepage").ids["perfilpage"].ids["id_usuario"].text = f'Seu ID Único é {id}'

            # preencher o nome do usuario
            nome = requisicao_dic["nome"]
            self.nome = nome
            self.root.get_screen("homepage").ids["perfilpage"].ids["nome"].text = nome

            # preencher o email do usuario, porém não tem email no banco de dados do usuário só no authenticatior do google
            email = "Sem email no banco de dados"
            self.email = email
            self.root.get_screen("homepage").ids["perfilpage"].ids["email"].text = email

            # preencher o telefone do usuario
            telefone = requisicao_dic["telefone"]
            self.telefone = telefone
            self.root.get_screen("homepage").ids["perfilpage"].ids["telefone"].text = telefone

            # preencher a localizacao do usuario
            localizacao = requisicao_dic["localizacao"]
            self.localizacao = localizacao
            self.root.get_screen("homepage").ids["perfilpage"].ids["localizacao"].text = localizacao

            # preencher a data de cadastro do usuario
            data_cadastro = requisicao_dic["data_criacao_de_conta"]
            self.data_cadastro = data_cadastro
            self.root.get_screen("homepage").ids["perfilpage"].ids["data_cadastro"].text = f"Data de Cadastro: {str(data_cadastro)}"

            # preencher o tipo de deficiencia do usuario
            tipo_deficiencia = requisicao_dic["deficiencia"]
            self.tipo_deficiencia = tipo_deficiencia
            self.root.get_screen("homepage").ids["perfilpage"].ids["tipo_deficiencia"].text = tipo_deficiencia

            # Quando preenchidas as informacoes, mudar para a homepage
            self.mudar_tela("homepage")
        
        # se nao tiver o arquivo de refresh token ou ocorrer outro erro, mudar para a tela de login e mostrar a excecao se for o segundo acesso do usuario ao app
        except Exception as excecao:
            print("Deu um erro ao carregar as informações do Usuário:", excecao)
            traceback.print_exc()

            try:
                # carrengado o email e senha do arquivo usuario.txt
                with open("usuario.txt", "r") as arquivo:
                    email, senha = arquivo.read().splitlines()
                # escrevendo nos campos de email e senha
                pagina_login = self.root.get_screen("loginpage")
                pagina_login.ids["email"].text = email
                pagina_login.ids["senha"].ids["text_field"].text = senha
                pagina_login.ids["caixa_selecao"].active = True

                self.visitas_app += 1
            except Exception as excecao:
                print("Deu um erro ao carregar o email e senha do arquivo usuario.txt:", excecao)
                traceback.print_exc()

            # se for a primeira vez entrando no app redirecionar para pagina de tutorialpage1
            if self.visitas_app == 0:
                # se for a segunda vez entrando no app redirecionar para pagina de startpage
                self.mudar_tela("tutorialpage1")
            else:
                self.mudar_tela("loginpage")

    def mudar_tela(self, nome_tela):
        # print(id_tela)
        gerenciador_telas = self.root
        gerenciador_telas.current = nome_tela
    
MainApp().run()