from kivymd.app import MDApp
# from kivy.core.window import Window
from telas import *
from botoes import *
from myfirebase import MyFirebase
import requests
import traceback
from kivymd.uix.menu import MDDropdownMenu
from gpshelper import *
# from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from linemaplayer import LineMapLayer
from api_rotas import GraphHopperAPI   

# Window.size = (360, 800) # tamanho da janela do aplicativo

class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Carregando arquivos kv
        self.load_all_kv_files(self.directory)
        # Gerenciador de Telas
        self.sm = MDScreenManager()
        self.firebase = MyFirebase()
        self.visitas_app = 0
        self.dialog = None

    def build(self):
        self.sm.add_widget(TutorialPage1(name='tutorialpage1'))
        self.sm.add_widget(TutorialPage2(name='tutorialpage2'))
        self.sm.add_widget(TutorialPage3(name='tutorialpage3'))
        self.sm.add_widget(StartPage(name='startpage'))
        self.sm.add_widget(CadastroPage(name='cadastropage'))
        self.sm.add_widget(LoginPage(name='loginpage'))
        self.sm.add_widget(HomePage(name='homepage'))
        return self.sm
    
    def on_start(self):
        # carrega o gps
        GpsHelper().run()
        # self.visitas_app += 1
        # carregar as informacoes do usuario
        self.carregar_info_usuario()
        # carregar os obstaculos do banco de dados
        self.carregar_obstaculos()
        # carrega a linha no mapa

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
            except:
                pass
            # except Exception as excecao:
            #     print("Deu um erro ao carregar o email e senha do arquivo usuario.txt:", excecao)
            #     traceback.print_exc()

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

            # preencher foto de perfil
            avatar = requisicao_dic["foto_de_perfil"]
            self.avatar = avatar
            foto_perfil = self.root.get_screen("homepage").ids["perfilpage"].ids["foto_perfil"]
            foto_perfil.source = f"icones/user/{avatar}"
            nome_foto_perfil =  self.root.get_screen("homepage").ids["perfilpage"].ids["nome_foto_perfil"]
            nome_foto_perfil.text = avatar

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
        except:
        # # se nao tiver o arquivo de refresh token ou ocorrer outro erro, mudar para a tela de login e mostrar a excecao se for o segundo acesso do usuario ao app
        # except Exception as excecao:
        #     print("Deu um erro ao carregar as informações do Usuário:", excecao)
        #     traceback.print_exc()

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
            except:
                pass
            # except Exception as excecao:
            #     print("Deu um erro ao carregar o email e senha do arquivo usuario.txt:", excecao)
            #     traceback.print_exc()

            # se for a primeira vez entrando no app redirecionar para pagina de tutorialpage1
            if self.visitas_app == 0:
                # se for a segunda vez entrando no app redirecionar para pagina de startpage
                self.mudar_tela("tutorialpage1")
            else:
                self.mudar_tela("loginpage")

    # Funcao para carregar os obstaculos do banco de dados
    def carregar_obstaculos(self):
        self.menu_items = [
            {
                "text": "Não Possuo",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Nao Possuo": self.menu_callback(x),
            },
            {
                "text": "Visual",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Visual": self.menu_callback(x),
            }, 
            {
                "text": "Auditiva",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Auditiva": self.menu_callback(x),
            },
            {
                "text": "Física",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Fisica": self.menu_callback(x),
            },
            {
                "text": "Intelectual",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Intelectual": self.menu_callback(x),
            },
            {
                "text": "Múltipla",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Multipla": self.menu_callback(x),
            },
        ]

        self.menu = MDDropdownMenu(
            caller=self.root.get_screen("homepage").ids["perfilpage"].ids["tipo_deficiencia"],
            items=self.menu_items,
            position="bottom",
            width_mult=4,
        )
        
    # Funcao para abrir o menu do tipo de deficiencia
    def menu_callback(self, text_item):
        self.root.get_screen("homepage").ids["perfilpage"].ids["tipo_deficiencia"].text = text_item
        self.menu.dismiss()

    # Funcao para abrir a nav_drawer da homepage
    def open_nav_drawer(self):
        self.root.get_screen("homepage").ids["nav_drawer"].set_state("open")

    # Função para trocar de screen no BottomNavigation
    def trocar_screen(self, nome_screen):
        self.root.get_screen("homepage").ids["barra_navegacao"].current = nome_screen

    # mensagem de popup generica para ser usada em qualquer situacao com botoes de ok e cancelar
    def mostrar_alerta(self, titulo, texto):
        if not self.dialog:
            self.dialog = MDDialog(
                title=f"{titulo}",
                text=f"{texto}",
            )
        self.dialog.open()

    # funcao para desenhar a rota no mapa
    def rota(self, partida, destino):
        # pegar as coordenadas de partida e destino
        try:
            if partida == destino:
                self.mostrar_alerta("Erro", "Partida e Destino não podem ser iguais")
            else:
                partida = partida
                destino = destino
                latitude1, longitude1 = partida.split(", ")
                latitude2, longitude2 = destino.split(", ")

                minhas_coordenadas = ([float(longitude1),float(latitude1)], [float(longitude2),float(latitude2)])

                dic_rota = GraphHopperAPI().get_route(points=minhas_coordenadas)
                self.dic_rota = dic_rota
                coordenadas_rota = dic_rota["paths"][0]["points"]["coordinates"]
                # invertendo a ordem de lat e lon para lon e lat
                for i in range(len(coordenadas_rota)):
                    coordenadas_rota[i] = [coordenadas_rota[i][1], coordenadas_rota[i][0]]

                line_layer = LineMapLayer(coordinates=coordenadas_rota, color=[1, 0, 0, 1])
                mapa = self.root.get_screen("homepage").ids["mapapage2"].ids["mapview"]
                mapa.add_layer(line_layer, mode="scatter")
        except Exception as excecao:
            print("Deu um erro ao desenhar a rota:", excecao)
            traceback.print_exc()
            self.mostrar_alerta("Erro", "Não foi possível desenhar a rota, Nome do erro:" + str(excecao)+"\n"+"Resposta da API"+"\n"+str(self.dic_rota))
    
    # Funcao para mudar de tela
    def mudar_tela(self, nome_tela):
        # print(id_tela)
        gerenciador_telas = self.root
        gerenciador_telas.current = nome_tela
    
MainApp().run()