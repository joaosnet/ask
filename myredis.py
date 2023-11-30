import redis
from datetime import datetime
import traceback    # Para mostrar o erro no console

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
            print("Deu um erro ao carregar os obstáculos do banco de dados:", excecao)
            traceback.print_exc()

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
            self.mostrar_alerta("Erro", f"Não foi possível adicionar o obstáculo\n{e}\n{tb}")

# Uso
if __name__ == '__main__':
    lat = -23.5629
    lon = -46.6544
    nome = 'Rua do Matão'
    manager = RedisManager('redis://wayway-001.shrvtq.0001.use1.cache.amazonaws.com:6379')
    manager.carregar_obstaculos()
    manager.adicionar_obstaculo('Perigoso', lat, lon, nome)
    manager.adicionar_obstaculo('Atenção', lat, lon, nome)
    manager.adicionar_obstaculo('Temporário', lat, lon, nome)
    manager.carregar_obstaculos()
