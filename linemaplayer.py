from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapLayer, MapMarker
from kivy.graphics import Color, Line
from kivy.graphics.context_instructions import Translate, Scale, PushMatrix, PopMatrix
from kivy_garden.mapview.utils import clamp
from kivy_garden.mapview.constants import \
    (MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE)
from math import radians, log, tan, cos, pi
import random


class LineMapLayer(MapLayer):
    """
    Classe que representa uma camada de mapa que desenha uma linha entre dois pontos.

    :param coordinates: Lista de coordenadas dos pontos que definem a linha.
    :type coordinates: list[list[float, float]]
    :param color: Cor da linha no formato RGBA.
    :type color: list[float]
    """

    def __init__(self, coordinates=[[0, 0], [0, 0]], color=[0, 0, 1, 1], **kwargs):
        super().__init__(**kwargs)
        self._coordinates = coordinates
        self.color = color
        self._line_points = None
        self._line_points_offset = (0, 0)
        self.zoom = 0
        self.lon = 0
        self.lat = 0
        self.ms = 0

    @property
    def coordinates(self):
        """
        Retorna as coordenadas dos pontos que definem a linha.

        :return: Lista de coordenadas dos pontos que definem a linha.
        :rtype: list[list[float, float]]
        """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        """
        Define as coordenadas dos pontos que definem a linha.

        :param coordinates: Lista de coordenadas dos pontos que definem a linha.
        :type coordinates: list[list[float, float]]
        """
        self._coordinates = coordinates
        self.invalidate_line_points()
        self.clear_and_redraw()

    @property
    def line_points(self):
        """
        Retorna os pontos que definem a linha.

        :return: Lista de pontos que definem a linha.
        :rtype: list[tuple[float, float]]
        """
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points

    @property
    def line_points_offset(self):
        """
        Retorna o deslocamento dos pontos que definem a linha.

        :return: Deslocamento dos pontos que definem a linha.
        :rtype: tuple[float, float]
        """
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset

    def calc_line_points(self):
        """
        Calcula os pontos que definem a linha.
        """
        # Desloca todos os pontos pelas coordenadas do primeiro ponto,
        # para manter as coordenadas mais próximas de zero.
        # (e, portanto, evitar alguns problemas de precisão de ponto flutuante ao desenhar linhas)
        self._line_points_offset = (self.get_x(self.coordinates[0][1]),
                                    self.get_y(self.coordinates[0][0]))
        # Como a latitude não é uma transformação linear, devemos calcular manualmente
        self._line_points = [(self.get_x(lon) - self._line_points_offset[0],
                              self.get_y(lat) - self._line_points_offset[1])
                             for lat, lon in self.coordinates]

    def invalidate_line_points(self):
        """
        Invalida os pontos que definem a linha.
        """
        self._line_points = None
        self._line_points_offset = (0, 0)

    def get_x(self, lon):
        """
        Obtém a posição x no mapa usando a projeção desta fonte de mapa.
        (0, 0) está localizado no canto superior esquerdo.

        :param lon: Longitude do ponto.
        :type lon: float
        :return: Posição x no mapa.
        :rtype: float
        """
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) * self.ms / 360.0

    def get_y(self, lat):
        """
        Obtém a posição y no mapa usando a projeção desta fonte de mapa.
        (0, 0) está localizado no canto superior esquerdo.

        :param lat: Latitude do ponto.
        :type lat: float
        :return: Posição y no mapa.
        :rtype: float
        """
        lat = radians(clamp(-lat, MIN_LATITUDE, MAX_LATITUDE))
        return (1.0 - log(tan(lat) + 1.0 / cos(lat)) / pi) * self.ms / 2.0

    def reposition(self):
        """
        Função chamada quando o MapView é movido.
        """
        map_view = self.parent

        # Deve redesenhar quando o zoom muda
        # pois a transformação de dispersão é redefinida para os novos azulejos
        if self.zoom != map_view.zoom or \
                   self.lon != round(map_view.lon, 7) or \
                   self.lat != round(map_view.lat, 7):
            map_source = map_view.map_source
            self.ms = pow(2.0, map_view.zoom) * map_source.dp_tile_size
            self.invalidate_line_points()
            self.clear_and_redraw()

    def clear_and_redraw(self, *args):
        """
        Limpa a linha antiga e redesenha a linha.
        """
        with self.canvas:
            # Limpa a linha antiga
            self.canvas.clear()

        self._draw_line()

    def _draw_line(self, *args):
        """
        Desenha a linha.
        """
        map_view = self.parent
        self.zoom = map_view.zoom
        self.lon = map_view.lon
        self.lat = map_view.lat

        # Ao fazer zoom, devemos desfazer a transformação de dispersão atual
        # ou a animação a distorce
        scatter = map_view._scatter
        sx, sy, ss = scatter.x, scatter.y, scatter.scale

        # Considera o tamanho do azulejo da fonte do mapa e o zoom da visualização do mapa
        vx, vy, vs = map_view.viewport_pos[0], map_view.viewport_pos[1], map_view.scale

        with self.canvas:

            # Salva o contexto do espaço de coordenadas atual
            PushMatrix()

            # Desloca pela posição do MapView na janela (sempre 0,0?)
            Translate(*map_view.pos)

            # Desfaz a transformação de animação de dispersão
            Scale(1 / ss, 1 / ss, 1)
            Translate(-sx, -sy)

            # Aplica o get window xy from transforms
            Scale(vs, vs, 1)
            Translate(-vx, -vy)

            # Aplica o que podemos fatorar da conversão de long, lat da fonte do mapa para x, y
            Translate(self.ms / 2, 0)

            # Desloca pelo deslocamento dos pontos da linha
            # (this keeps the points closer to the origin)
            Translate(*self.line_points_offset)

            Color(*self.color)
            Line(points=self.line_points, width=2)

            # Retrieve the last saved coordinate space context
            PopMatrix()


class MapLayout(Screen):
    pass


class MapViewApp(MDApp):
    def on_start(self):
        mapview = self.root.mapview

        mapview.lat = 51.046284
        mapview.lon = 1.541179
        mapview.zoom = 7             # zoom values: 0 - 19

        # You can import JSON data here or:
        my_coordinates = [[51.505807, -0.128513], [51.126251, 1.327067],
                          [50.959086, 1.827652], [48.85519, 2.35021]]

        # Add routes
        lml1 = LineMapLayer(coordinates=my_coordinates, color=[1, 0, 0, 1])
        mapview.add_layer(lml1, mode="scatter")

        my_coordinates = [my_coordinates[-1]]
        for i in range(4600):
            my_coordinates.append(gen_rand_point(my_coordinates[-1]))
        lml2 = LineMapLayer(coordinates=my_coordinates, color=[0.5, 0, 1, 1])
        mapview.add_layer(lml2, mode="scatter")

        my_coordinates = [[51.505807, -0.128513], [48.85519, 2.35021]]
        lml3 = LineMapLayer(coordinates=my_coordinates, color=[0, 0, 1, 1])
        mapview.add_layer(lml3, mode="scatter")

        # Add markers
        marker = MapMarker(lat=51.126251, lon=1.327067, source='images/marker.png')
        mapview.add_marker(marker)

        marker = MapMarker(lat=50.959086, lon=1.827652, source='images/marker.png')
        mapview.add_marker(marker)

    def build(self):
        return MapLayout()
    
def gen_rand_point(last_coordinate):
    dx, dy = random.randint(-100, 100) / 10000.0, random.randint(0, 100) / 10000.0
    c = (last_coordinate[0] + dx,
         last_coordinate[1] + dy)
    return c


if __name__ == '__main__':
    MapViewApp().run()