from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy_garden.mapview import MapMarkerPopup
from kivymd.uix.dialog import MDDialog

class AccessibleMapView(MapView):
    getting_markets_timer = None
    market_names = []

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
        Obtém os mercados acessíveis na área de visualização.

        Este método obtém a referência para o aplicativo principal e o cursor do banco de dados.
        Em seguida, executa uma consulta SQL para obter os mercados que estão dentro da área de visualização.
        Os mercados obtidos são impressos no console e adicionados ao mapa como marcadores acessíveis.
        """
        min_lat, min_lon, max_lat, max_lon = self.get_bbox()
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM markets WHERE x > %s AND x < %s AND y > %s AND y < %s "%(min_lon, max_lon, min_lat, max_lat)
        app.cursor.execute(sql_statement)
        markets = app.cursor.fetchall()
        print(markets)
        for market in markets:
            name = market[1]
            if name in self.market_names:
                continue
            else:
                self.add_accessible_market(market)

    def add_accessible_market(self, market):
        """
        Adiciona um mercado acessível ao mapa.

        Este método cria um marcador de mercado acessível com base nas coordenadas fornecidas.
        Em seguida, o marcador é adicionado ao mapa e o nome do mercado é armazenado para controle.
        """
        lat, lon = market[21], market[20]
        marker = AccessibleMarketMarker(lat=lat, lon=lon)
        marker.market_data = market
        self.add_widget(marker)
        name = market[1]
        self.market_names.append(name)

class AccessibleMarketMarker(MapMarkerPopup):
    # Implementar funcionalidades específicas para um MarketMarker acessível
    source = "marker.png"
    market_data = []

    def on_release(self):
        # Open up the LocationPopupMenu
        menu = LocationPopupMenu(self.market_data)
        menu.size_hint = [.8, .9]
        menu.open()

class LocationPopupMenu(MDDialog):
    def __init__(self, market_data):
        super().__init__()

        # Set all of the fields of market data
        headers = "FMID,MarketName,Website,Facebook,Twitter,Youtube,OtherMedia,street,city,County,State,zip,Season1Date,Season1Time,Season2Date,Season2Time,Season3Date,Season3Time,Season4Date,Season4Time,x,y,Location,Credit,WIC,WICcash,SFMNP,SNAP,Organic,Bakedgoods,Cheese,Crafts,Flowers,Eggs,Seafood,Herbs,Vegetables,Honey,Jams,Maple,Meat,Nursery,Nuts,Plants,Poultry,Prepared,Soap,Trees,Wine,Coffee,Beans,Fruits,Grains,Juices,Mushrooms,PetFood,Tofu,WildHarvested,updateTime"
        headers = headers.split(',')

        for i in range(len(headers)):
            attribute_name = headers[i]
            attribute_value = market_data[i]
            setattr(self, attribute_name, attribute_value)





