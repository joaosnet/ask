import requests
from kivymd.app import MDApp
import redis
class GraphHopperAPI:
    """
    Classe que representa a API do GraphHopper.

    Atributos:
        url (str): URL base da API.
        query (dict): Dicionário com os parâmetros da query string.
        headers (dict): Dicionário com os headers da requisição.

    Métodos:
        get_route: Retorna a rota entre dois pontos.
    """
    def __init__(self):
        
        """
        Inicializa a classe GraphHopperAPI com os atributos padrão.
        """
        self.url = "https://graphhopper.com/api/1/"
        self.query = {"key": "17e8fe9c-35aa-47cb-9c6b-3fbb62b7259b"}
        self.headers = {"Content-Type": "application/json"}
        # self.rc = redis.Redis.from_url('redis://44.221.222.136:6379', password='inclusivewaydb1019')
        # self.lon = -48.45160647253775
        # self.lat = -1.474081251977831
        # self.radius = 100000
        # self.unit = "km"
        # self.tipos = ["Perigoso", "Atenção", "Temporário"]
        # self.obstaculos = []

    def get_route(self, points, vehicle="foot"):
        """
        Retorna a rota entre dois pontos.

        Args:
            points (list): Lista com as coordenadas dos pontos de origem e destino.
            vehicle (str): Tipo de veículo utilizado na rota. Padrão é "foot" (a pé).

        Returns:
            dict: Dicionário com as informações da rota.
        """
        # verifica se tem algum obstáculo no caminho com o redis se tiver adiciona
        app = MDApp.get_running_app()
        mapa = app.root.get_screen("homepage").ids["mapapage2"].ids["mapview"]
        longitude = mapa.lon
        latitude = mapa.lat
        # longitude = self.lon
        # latitude = self.lat
        # Atualiza o raio para um valor baseado no nível de zoom do mapa
        # Este é apenas um exemplo, você pode querer ajustar o cálculo para se adequar às suas necessidades
        radius = 10000 * (1 / mapa.zoom)
        # pp(radius)
        tipos = ["Perigoso", "Atenção", "Temporário"]
        # Define o tamanho do quadrado (em graus)
        tamanho_quadrado = 0.01  # Ajuste este valor conforme necessário

        for tipo in tipos:
            # Busca os obstáculos do tipo atual no banco de dados Redis
            obstaculos_redis = app.rc.georadius(
                name=tipo,
                longitude=longitude,
                latitude=latitude,
                radius=self.radius,
                unit="km",
            )
            obstaculos_redis = [[tipo, obstaculo, app.rc.geopos(tipo, obstaculo)[0]] for obstaculo in obstaculos_redis]
            if obstaculos_redis != []:
                print(obstaculos_redis)
                # Inicializa o dicionário obstaculos com o modelo
                obstaculos = {
                    "speed": [
                    ],
                    "areas": {
                        "type": "FeatureCollection",
                        "features": []
                    }
                }
                # Adiciona os obstáculos ao dicionário
                for i, obstaculo in enumerate(obstaculos_redis):
                    # Calcula as coordenadas do quadrado
                    tipo, informacoes, coords = obstaculo
                    lon, lat = coords
            
                    # como as informacoes estao b'0.1,04/12/2023 11:08:58,Neto'
                    # precisamos converter formatar separadamente em variaveis
                    informacoes = informacoes.decode('utf-8')
                    informacoes = informacoes.split(',')
                    speed_multiplier = informacoes[0]
                    nome_custom = "custom" + str(i + 1)
                    quadrado = [
                        [lon - tamanho_quadrado, lat - tamanho_quadrado],
                        [lon + tamanho_quadrado, lat - tamanho_quadrado],
                        [lon + tamanho_quadrado, lat + tamanho_quadrado],
                        [lon - tamanho_quadrado, lat + tamanho_quadrado],
                        [lon - tamanho_quadrado, lat - tamanho_quadrado],  # Fecha o polígono
                    ]
                    # Adiciona a velocidade da pista ao dicionário de obstáculos
                    obstaculos["speed"].append({
                        "if": "in_" + nome_custom,
                        "multiply_by": speed_multiplier
                    })

                    # Adiciona o quadrado à lista de "features"
                    obstaculos["areas"]["features"].append({
                        "type": "Feature",
                        "id": nome_custom,
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [quadrado]
                        }
                    })
                # montando a payload da requisicao  
                payload = {
                    "points": points,
                    "details": ["road_class","surface"],
                    "vehicle": vehicle,
                    "locale": "pt_BR",
                    "instructions": True,
                    "calc_points": True,
                    "points_encoded": False,
                    "custom_model": obstaculos,
                    "ch.disable": True,
                }
            else:
                payload = {
                    "points": points,
                    "details": ["road_class","surface"],
                    "vehicle": vehicle,
                    "locale": "pt_BR",
                    "instructions": True,
                    "calc_points": True,
                    "points_encoded": False,
                }

        response = requests.post(self.url + "route", json=payload, headers=self.headers, params=self.query)
        data = response.json()
        return data
    
            
# Exemplo de uso
if __name__ == '__main__':
    rota = GraphHopperAPI().get_route(points=([-48.450860,-1.323304],[-48.451630,-1.473959]))
    from pprint import pprint as pp
    if 'paths' in rota:
        pp(rota["paths"][0]["points"]["coordinates"])
    else:
        pp(rota)


