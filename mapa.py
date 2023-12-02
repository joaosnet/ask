from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.dialog import MDDialog
import traceback
import redis
from pprint import pprint as pp
from kivymd.uix.button import MDFlatButton

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
            rc =  redis.Redis.from_url('redis://44.221.222.136:6379')
            longitude = self.lon
            latitude = self.lat
            # Atualiza o raio para um valor baseado no nível de zoom do mapa
            # Este é apenas um exemplo, você pode querer ajustar o cálculo para se adequar às suas necessidades
            radius = 1000 * (2 / self.zoom)
            pp(radius)
            tipos = ["Perigoso", "Atenção", "Temporário"]
            for tipo in tipos:
                obstaculos = rc.georadius(
                    name=tipo,
                    longitude=longitude,
                    latitude=latitude,
                    radius=radius,
                    unit="km",
                )
                obstaculos = [[tipo, obstaculo, app.rc.geopos(tipo, obstaculo)[0]] for obstaculo in obstaculos]
                # pp(obstaculos)
                # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                for obstaculo in obstaculos:
                    tipo, info, coords = obstaculo
                    # pp(coords)
                    # pp(self.informacoes)
                    if info in self.informacoes:
                        continue
                    else:
                        self.add_accessible_market(obstaculo)
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
        tipo, name, coords = market
        lon, lat = coords
        marker = AccessibleMarketMarker(lat=lat, lon=lon)
        marker.market_data = market
        self.add_widget(marker)
        self.informacoes.append(coords)

class AccessibleMarketMarker(MapMarkerPopup):
    # Implementar funcionalidades específicas para um MarketMarker acessível
    source = "icones/Marker.png"
    market_data = []

    def on_release(self):
        # Open up the LocationPopupMenu
        menu = LocationPopupMenu(self.market_data)
        # menu.size_hint = [.8, .9]
        menu.open()

class LocationPopupMenu(MDDialog):
    def __init__(self, market_data):
        super().__init__()

        # Set all of the fields of market data
        headers = "tipo,name,coords"
        headers = headers.split(',')

        for i in range(len(headers)):
            attribute_name = headers[i]
            attribute_value = market_data[i]
            # Decodifica o nome se ele for uma string codificada em bytes
            if attribute_name == 'name' and isinstance(attribute_value, bytes):
                attribute_value = attribute_value.decode('utf-8')
            setattr(self, attribute_name, attribute_value)

        # Define o título e o texto do diálogo
        titulo = self.name
        texto = f"Tipo: {self.tipo}\nCoordenadas: {self.coords}"

        # Cria e abre o diálogo
        self.title = titulo
        self.text = texto
        self.buttons = [
            MDFlatButton(
                text="OK", text_color=self.theme_cls.primary_color, on_release= lambda _: self.dismiss()
            ),
        ]
        self.open()




