from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.dialog import MDDialog
import traceback
import redis
# from pprint import pprint as pp
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty

class AccessibleMapView(MapView):
    getting_markets_timer = None
    informacoes = []

    def start_getting_markets_in_fov(self):
        """
        Inicia o temporizador para obter os mercados na área de visualização.

        Este método cancela o temporizador existente, se houver, e inicia um novo temporizador
        que chama o método get_accessible_markets_in_fov após um segundo.
        """
        try:
            self.getting_markets_timer.cancel()
        except:
            pass

        self.getting_markets_timer = Clock.schedule_once(self.get_accessible_markets_in_fov, 1)

    def get_accessible_markets_in_fov(self, *args):
        """
        Obtém os obstáculos na área de visualização.

        Este método obtém a referência para o aplicativo principal e o cliente Redis.
        Em seguida, usa o método georadius para obter os obstáculos dentro de um raio específico.
        Os obstáculos obtidos são impressos no console e adicionados ao mapa como marcadores acessíveis.
        """
        try:
            app = MDApp.get_running_app()
            # Atualiza a longitude e a latitude para a localização atual do mapa
            lat, lon = app.gps.get_lat_lon()
            longitude = lon
            latitude = lat
            # Atualiza o raio para um valor baseado no nível de zoom do mapa
            # Este é apenas um exemplo, você pode querer ajustar o cálculo para se adequar às suas necessidades
            radius = 500
            # pp(radius)
            tipos = ["Perigoso", "Atenção", "Temporário"]
            for tipo in tipos:
                obstaculos = app.rc.georadius(
                    name=tipo,
                    longitude=longitude,
                    latitude=latitude,
                    radius=radius,
                    unit="m",
                )
                obstaculos = [[tipo, obstaculo, app.rc.geopos(tipo, obstaculo)[0]] for obstaculo in obstaculos]
                # pp(obstaculos)
                # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                # Se tiver algum obstaculo no caminho adiciona
                if obstaculos != []:
                    for obstaculo in obstaculos:
                        tipo, info, coords = obstaculo
                        # pp(coords)
                        # pp(self.informacoes)
                        contador = 0
                        if info in self.informacoes:
                            print("O obstaculo já foi carregado")
                            if contador == 0:
                                self.add_accessible_market(obstaculo)
                                contador += 1
                            continue
                        else:
                            print("Carregando obstaculo")
                            self.add_accessible_market(obstaculo)
                            if contador == 1:
                                contador -= 1
        except Exception as excecao:
            tb = traceback.format_exc()
            print("O erro de carregar obstaculo está aqui: ", excecao)
            print("O traceback está aqui: ", tb)
            
    def add_accessible_market(self, market):
        """
        Adiciona um mercado acessível ao mapa.

        Este método cria um marcador de mercado acessível com base nas coordenadas fornecidas.
        Em seguida, o marcador é adicionado ao mapa e o nome do mercado é armazenado para controle.
        """
        # pp(market)
        # print("----------------------------")
        tipo, info, coords = market
        lon, lat = coords
        marker = AccessibleMarketMarker(lat=lat, lon=lon, tipo=tipo)
        marker.market_data = market
        self.add_widget(marker)
        self.informacoes.append(info)

class AccessibleMarketMarker(MapMarkerPopup):
    tipo = StringProperty()
    market_data = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.tipo == "Perigoso":
            self.source = f"icones/perigoso.png"
        elif self.tipo == "Atenção":
            self.source = f"icones/atencao.png"
        else:
            self.source = f"icones/temporario.png"
        self.size = (100, 100)

    def on_release(self):
        menu = LocationPopupMenu(self.market_data)
        menu.open()

class LocationPopupMenu(MDDialog):
    def __init__(self, market_data):
        super().__init__()

        # Extrai os dados do mercado
        tipo, informacoes, coords = market_data
        
        # como as informacoes estao b'0.1,04/12/2023 11:08:58,Neto'
        # precisamos converter formatar separadamente em variaveis
        informacoes = informacoes.decode('utf-8')
        informacoes = informacoes.split(',')

        lat, lon = coords

        # Define o título e o texto do diálogo
        titulo = f"Informações do Obstáculo"
        texto = f"Tipo: {tipo}\nCoordenadas: {lat}, {lon}\nNome do Usuário que adicionou o obstaculo: {informacoes[2]}\nData da adição: {informacoes[1]}\nVelocidade da Pista: {informacoes[0]}"

        # Cria e abre o diálogo
        self.title = titulo
        self.text = texto
        self.open()

class carregando(MDDialog):
    def __init__(self):
        super().__init__()

        # Define o título e o texto do diálogo
        titulo = f"Carregando Obstáculos"

        # Cria e abre o diálogo
        self.title = titulo
        # self.Image: source: "icones\Gps.png"
        self.open()


