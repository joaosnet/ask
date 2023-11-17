import requests

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
        self.url = "https://graphhopper.com/api/1/route"
        self.query = {"key": "17e8fe9c-35aa-47cb-9c6b-3fbb62b7259b"}
        self.headers = {"Content-Type": "application/json"}

    def get_route(self, points, vehicle="foot"):
        """
        Retorna a rota entre dois pontos.

        Args:
            points (list): Lista com as coordenadas dos pontos de origem e destino.
            vehicle (str): Tipo de veículo utilizado na rota. Padrão é "foot" (a pé).

        Returns:
            dict: Dicionário com as informações da rota.
        """
        payload = {
            "points": points,
            "details": ["road_class","surface"],
            "vehicle": vehicle,
            "locale": "pt_BR",
            "instructions": True,
            "calc_points": True,
            "points_encoded": False
        }
        response = requests.post(self.url, json=payload, headers=self.headers, params=self.query)
        data = response.json()
        return data
    
# Exemplo de uso
if __name__ == '__main__':
    gh = GraphHopperAPI().get_route(points=([-48.450860,-1.323304],[-48.451630,-1.473959]))
    from pprint import pprint as pp
    pp(gh["paths"][0]["points"]["coordinates"])


