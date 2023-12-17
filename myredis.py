# essa classe deve ter funcoes para o o gerenciamento do banco de dados redis
import redis
from pprint import pprint as pp
from segredos import PASSWORD

# iniciar o banco de dados redis
class MyRedis():
    def __init__(self):
        self.rc = redis.Redis.from_url('redis://44.221.222.136:6379', password=PASSWORD)
        self.longitude = -48.45160647253775
        self.latitude = -1.474081251977831
        self.radius = 100000
        self.unit = "km"
        self.tipos = ["Perigoso", "Atenção", "Temporário"]
        self.obstaculos = []

    # Procurar por todos os obstaculos no banco de dados
    def get_obstaculos(self):
        for tipo in self.tipos:
            obstaculos = self.rc.georadius(
                name=tipo,
                longitude=self.longitude,
                latitude=self.latitude,
                radius=self.radius,
                unit=self.unit,
            )
            obstaculos = [[tipo, obstaculo, self.rc.geopos(tipo, obstaculo)[0]] for obstaculo in obstaculos]
            self.obstaculos.append(obstaculos)
        return self.obstaculos
    
# Exemplos de uso:
if __name__ == "__main__":
    pp(MyRedis().get_obstaculos())