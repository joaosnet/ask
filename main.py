from kivymd.app import MDApp
from telas import *
from botoes import *
from myfirebase import MyFirebase
import requests
from kivymd.uix.menu import MDDropdownMenu
from gpshelper import *
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from linemaplayer import LineMapLayer
from api_rotas import GraphHopperAPI
from pesquisa import SearchTextInput, Search_Select_Option
from kivy.properties import ListProperty
import os
from functools import partial
from kivy.network.urlrequest import UrlRequest
from threading import Thread
import json
import certifi
from datetime import datetime
import traceback
import redis
from mapa import AccessibleMapView, AccessibleMarketMarker, LocationPopupMenu

os.environ["SSL_CERT_FILE"] = certifi.where()

class MainApp(MDApp):
    """
    Classe principal da aplicação.
    """
    DEBUG = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipos_obstaculos = {
            'Perigoso': [
                'close-octagon',
                "on_release", lambda x: self.adicionar_obstaculo("Perigoso", self.nome),
            ],
            'Atenção': [
                'alert-circle',
                "on_release", lambda x: self.adicionar_obstaculo("Atenção", self.nome)
            ],
            'Temporário': [
                'clock-fast',
                "on_release", lambda x: self.adicionar_obstaculo("Temporário", self.nome)
            ],
        }
        # Carregando arquivos kv
        self.load_all_kv_files(self.directory)
        # Gerenciador de Telas
        self.sm = MDScreenManager()
        self.firebase = MyFirebase()
        self.visitas_app = 0
        self.dialog = None
        self.gps = GpsHelper()
        self.rotas = GraphHopperAPI()
        self.rc =  redis.Redis.from_url('redis://44.221.222.136:6379', password='inclusivewaydb1019')

    def build(self):
        """
        Constrói a interface da aplicação.
        """
        self.sm.add_widget(TutorialPage1(name='tutorialpage1'))
        self.sm.add_widget(TutorialPage2(name='tutorialpage2'))
        self.sm.add_widget(TutorialPage3(name='tutorialpage3'))
        self.sm.add_widget(StartPage(name='startpage'))
        self.sm.add_widget(CadastroPage(name='cadastropage'))
        self.sm.add_widget(LoginPage(name='loginpage'))
        self.sm.add_widget(HomePage(name='homepage'))
        self.sm.add_widget(FotoPerfilPage(name='fotoperfilpage'))
        return self.sm
    
    def on_start(self):
        """
        Executado quando a aplicação é iniciada.
        """
        # Carregar as fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.get_screen("fotoperfilpage")
        lista_fotos = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            image = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(image)
        # Carrega o GPS
        self.gps.run()
        # self.visitas_app += 1
        # Carregar as informações do usuário
        self.carregar_info_usuario()
        # Carregar os obstáculos do banco de dados
        # self.rc = self.redis
        # self.carregar_obstaculos()

        self.menu_cadastro = self.create_menu(self.root.get_screen("cadastropage").ids["tipo_deficiencia"])
        self.menu_perfil = self.create_menu(self.root.get_screen("homepage").ids["perfilpage"].ids["tipo_deficiencia"])

    rv_data = ListProperty()

    def update_data(self, rv_data_list):
        """
        Atualiza os dados da lista de exibição.
        """
        self.rv_data = [{'text': item[0], "secondary_text": f"{item[1]['lat']}, {item[1]['lng']}"} for item in rv_data_list]
        # print(self.rv_data, 'update')

    def carregar_info_usuario(self):
        """
        Carrega as informações do usuário.
        """
        try:
            try:
                # Carregando o email e senha do arquivo usuario.txt
                with open("usuario.txt", "r") as arquivo:
                    email, senha = arquivo.read().splitlines()
                # Escrevendo nos campos de email e senha
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
            # Pegar informações do usuário
            link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()
            # pp(requisicao_dic)

            # Preencher foto de perfil
            avatar = requisicao_dic["foto_de_perfil"]
            self.avatar = avatar
            foto_perfil = self.root.get_screen("homepage").ids["perfilpage"].ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # Preencher o ID Único do usuário
            id = requisicao_dic["id"]
            self.id = id
            self.root.get_screen("homepage").ids["perfilpage"].ids["id_usuario"].text = f'Seu ID Único é {id}'

            # Preencher o nome do usuário
            nome = requisicao_dic["nome"]
            self.nome = nome
            self.root.get_screen("homepage").ids["perfilpage"].ids["nome"].text = nome

            # Preencher o email do usuário, porém não tem email no banco de dados do usuário só no authenticatior do google
            url = f'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=AIzaSyCL5SzpjM8b1VlO6XSwniNFplITXo99Xmo'
            headers = {'Content-Type': 'application/json'}
            data = {'idToken': id_token}
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_data = response.json()
            email = response_data['users'][0]['email']
            self.email = email
            self.root.get_screen("homepage").ids["perfilpage"].ids["email"].text = email

            # Preencher o telefone do usuário
            telefone = requisicao_dic["telefone"]
            self.telefone = telefone
            self.root.get_screen("homepage").ids["perfilpage"].ids["telefone"].text = telefone

            # Preencher a localização do usuário
            localizacao = requisicao_dic["localizacao"]
            self.localizacao = localizacao
            self.root.get_screen("homepage").ids["perfilpage"].ids["localizacao"].text = localizacao

            # Preencher a data de cadastro do usuário
            data_cadastro = requisicao_dic["data_criacao_de_conta"]
            self.data_cadastro = data_cadastro
            self.root.get_screen("homepage").ids["perfilpage"].ids["data_cadastro"].text = f"Data de Cadastro: {str(data_cadastro)}"

            # Preencher o tipo de deficiência do usuário
            tipo_deficiencia = requisicao_dic["deficiencia"]
            self.tipo_deficiencia = tipo_deficiencia
            self.root.get_screen("homepage").ids["perfilpage"].ids["tipo_deficiencia"].text = tipo_deficiencia

            # Quando preenchidas as informações, mudar para a homepage
            self.mudar_tela("homepage")
        except:
        # # Se não tiver o arquivo de refresh token ou ocorrer outro erro, mudar para a tela de login e mostrar a exceção se for o segundo acesso do usuário ao app
        # except Exception as excecao:
        #     print("Deu um erro ao carregar as informações do Usuário:", excecao)
        #     traceback.print_exc()

            try:
                # Carregando o email e senha do arquivo usuario.txt
                with open("usuario.txt", "r") as arquivo:
                    email, senha = arquivo.read().splitlines()
                # Escrevendo nos campos de email e senha
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

            # Se for a primeira vez entrando no app redirecionar para página de tutorialpage1
            if self.visitas_app == 0:
                # Se for a segunda vez entrando no app redirecionar para página de startpage
                self.mudar_tela("tutorialpage1")
            else:
                self.mudar_tela("loginpage")

    def create_menu(self, caller):
        self.menu = MDDropdownMenu(
            caller=caller,
            position="center",
            width=self.root.width,
        )

        menu_items = [
            {
                "text": tipo,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=tipo, menu=self.menu: self.menu_callback(x, menu, caller),
            }
            for tipo in ["Nao Possuo", "Visual", "Auditiva", "Fisica", "Intelectual", "Multipla"]
        ]

        self.menu.items = menu_items
        return self.menu

    def menu_callback(self, text_item, menu, caller):
        """
        Callback para o menu do tipo de deficiência.
        """
        caller.text = text_item
        menu.dismiss()

    def open_nav_drawer(self):
        """
        Abre a nav_drawer da homepage.
        """
        self.root.get_screen("homepage").ids["nav_drawer"].set_state("open")

    def trocar_screen(self, nome_screen):
        """
        Troca a tela no BottomNavigation.
        """
        self.root.get_screen("homepage").ids["barra_navegacao"].current = nome_screen

    def mostrar_alerta(self, titulo, texto):
        """
        Mostra um alerta genérico com botões de OK e Cancelar.
        """
        if not self.dialog:
            self.dialog = MDDialog(
                title=f"{titulo}",
                text=f"{texto}",
                buttons=[
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color, on_release= lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()

    def rota(self, partida, destino):
        """
        Desenha a rota no mapa.
        """
        # Pegar as coordenadas de partida e destino
        try:
            if partida == destino:
                self.mostrar_alerta("Erro", "Partida e Destino não podem ser iguais")
            elif partida == "" or destino == "":
                partida = self.root.get_screen("homepage").ids["mapapage2"].ids["Partida"]
                destino = self.root.get_screen("homepage").ids["mapapage2"].ids["Destino"]
                
                partida.helper_text_mode = "on_error"
                partida.helper_text = "Não pode ser vazio"
                partida.error = True

                destino.helper_text = "Não pode ser vazio"
                destino.helper_text_mode = "on_error"
                destino.error = True
            else:
                if partida == "Minha Localização atual":
                    latitude1, longitude1 = self.gps.get_lat_lon()
                else:
                    latitude1, longitude1 = partida.split(", ")

                destino = destino.split(":")

                latitude2, longitude2 = destino[0].split(", ")

                minhas_coordenadas = ([float(longitude1),float(latitude1)], [float(longitude2),float(latitude2)])

                dic_rota = self.rotas.get_route(points=minhas_coordenadas)

                coordenadas_rota = dic_rota["paths"][0]["points"]["coordinates"]
                # Invertendo a ordem de lat e lon para lon e lat
                for i in range(len(coordenadas_rota)):
                    coordenadas_rota[i] = [coordenadas_rota[i][1], coordenadas_rota[i][0]]
                line_layer = LineMapLayer(coordinates=coordenadas_rota, color=[1, 0, 0, 1])
                mapa = self.root.get_screen("homepage").ids["mapapage2"].ids["mapview"]
                mapa.add_layer(line_layer, mode="scatter")

                #Voltando para o MDBackdropFrontLayer
                self.root.get_screen("homepage").ids["mapapage2"].ids["backdrop"].open()
        except:
            self.mostrar_alerta("Erro", f"Não foi possível desenhar a rota\nVerifique se os campos de partida e destino estão preenchidos corretamente")
    # Funcao para mostrar a localizacao do usuario na caixa de texto partida
    def mostrar_localizacao_partida(self):
        try:
            # pegar a latitude e longitude do usuario
            self.lat, self.lon = self.gps.get_lat_lon()
            local = f"{self.lat}, {self.lon}"
            # colocar a latitude e longitude na caixa de texto partida
            self.root.get_screen("homepage").ids["mapapage2"].ids["Partida"].text = "Minha Localização atual"
            self.root.get_screen("homepage").ids["perfilpage"].ids["localizacao"].text = local
            link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
            info = f'{{"localizacao": "{local}"}}'
            Thread(target=requests.patch, args=(link,), kwargs={"data": info}).start()

        except:
                partida = self.root.get_screen("homepage").ids["mapapage2"].ids["Partida"]
                partida.helper_text_mode = "on_error"
                partida.helper_text = "Não foi possível pegar sua localização"
                partida.error = True    

    def mudar_foto_perfil(self, foto, *args):
        foto_perfil = self.root.get_screen("homepage").ids["perfilpage"].ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}"
        info = f'{{"foto_de_perfil": "{foto}"}}'
        requisicao = requests.patch(link, data = info)

        self.mudar_tela("homepage")

    def centralizar_mapa(self):
        try:
            lat, lon = self.gps.get_lat_lon()
            self.root.get_screen("homepage").ids["mapapage1"].ids["mapview"].center_on(lat, lon)
            self.root.get_screen("homepage").ids["mapapage2"].ids["mapview"].center_on(lat, lon)
        except: 
            self.gps.open_gps_access_popup()
    # Funcao para mudar de tela
    def mudar_tela(self, nome_tela):
        # print(id_tela)
        gerenciador_telas = self.root
        gerenciador_telas.current = nome_tela

    def adicionar_obstaculo(self, texto, nome):
        try:
            try:
                lat, lon = self.gps.get_lat_lon()
            except:
                lat, lon = self.root.get_screen("homepage").ids["mapapage1"].ids["mapview"].center
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if texto == 'Perigoso':
                speed = 0.1
            elif texto == 'Atenção':
                speed = 0.5
            elif texto == 'Temporário':
                speed = 0.7
            self.rc.geoadd(f"{texto}", [lon, lat, f'{speed},{data},{nome}'])
            MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["mapview"].get_accessible_markets_in_fov()
        except Exception as e: 
            tb = traceback.format_exc()
            self.mostrar_alerta("Erro", f"Não foi possível adicionar o obstáculo\n{e}\n{tb}")

MainApp().run()