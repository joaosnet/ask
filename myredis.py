# Biblitecas do HotReload
from kaki.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from botoes import *
from telas import *
from gpshelper import GpsHelper
from gpsblinker import GpsBlinker
from pesquisa import Search_Select_Option, SearchTextInput
from kivy_garden.mapview import MapView
from kivymd.uix.menu import MDDropdownMenu
import os
from mapa import AccessibleMapView
# Bibliotecas do RedisManager
import redis
from datetime import datetime
import traceback    # Para mostrar o erro no console
from pprint import pprint as pp

class RedisManager:
    def __init__(self, url):
        self.rc = redis.Redis.from_url(url)

    def carregar_obstaculos(self):
        """
        Carrega os obstáculos do banco de dados do redis.
        """
        try:
            obstaculos = self.rc.keys()
            obstaculos = [obstaculo.decode() for obstaculo in obstaculos]
            obstaculos = [obstaculo.split(',') for obstaculo in obstaculos]
            obstaculos = [[obstaculo[0], {'lat': obstaculo[1], 'lng': obstaculo[2]}] for obstaculo in obstaculos]
            self.update_data(obstaculos)
        except Exception as excecao:
            tb = traceback.format_exc()
            pp("O erro de carregar obstaculo está aqui: ", excecao)
            pp("O traceback está aqui: ", tb)

    def adicionar_obstaculo(self, texto, lat, lon, nome):
        try:
            data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if texto == 'Perigoso':
                speed = 0.1
            elif texto == 'Atenção':
                speed = 0.5
            elif texto == 'Temporário':
                speed = 0.7
            self.rc.set(f'{lat},{lon}', f'{texto},{speed},{data},{nome}')
        except Exception as e:
            tb = traceback.format_exc()
            pp("O erro de adicionar obstaculo está aqui:", e)
            pp("O traceback está aqui:", tb)

class HotReload(App, MDApp):
    DEBUG = True
    AUTORELOADER_PATHS = [
        (os.getcwd(), {'recursive': True}),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis = RedisManager('redis://wayway-001.shrvtq.0001.use1.cache.amazonaws.com:6379')
        self.tipos_obstaculos = {
            'Perigoso': [
                'close-octagon',
                "on_release", lambda x: self.redis.adicionar_obstaculo("Perigoso", -23.5629, -46.6544, 'Rua do Matão'),
            ],
            'Atenção': [
                'alert-circle',
                "on_release", lambda x: self.redis.adicionar_obstaculo("Atenção", -23.5629, -46.6544, 'Rua do Matão')
            ],
            'Temporário': [
                'clock-fast',
                "on_release", lambda x: self.redis.adicionar_obstaculo("Temporário", -23.5629, -46.6544, 'Rua do Matão')
            ],
        }    

    def build_app(self):
        return Builder.load_file('kv\mapage1.kv')            

# Uso
if __name__ == '__main__':
    HotReload().run()
