from kivy_garden.mapview import MapLayer
from kivy.graphics import Color, Line
from kivy.graphics.context_instructions import Translate, Scale, PushMatrix, PopMatrix
from kivy_garden.mapview.utils import clamp
from kivy_garden.mapview.constants import \
    (MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE)
from math import radians, log, tan, cos, pi

class LineMapLayer(MapLayer):
    """
    Classe que representa uma camada de mapa que desenha uma linha entre dois pontos geográficos.

    :param coordinates: Lista de coordenadas geográficas dos pontos da linha.
    :type coordinates: list
    :param color: Cor da linha no formato RGBA.
    :type color: list
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
        Retorna as coordenadas geográficas dos pontos da linha.

        :return: Lista de coordenadas geográficas dos pontos da linha.
        :rtype: list
        """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        """
        Define as coordenadas geográficas dos pontos da linha.

        :param coordinates: Lista de coordenadas geográficas dos pontos da linha.
        :type coordinates: list
        """
        self._coordinates = coordinates
        self.invalidate_line_points()
        self.clear_and_redraw()

    @property
    def line_points(self):
        """
        Retorna os pontos da linha em coordenadas de tela.

        :return: Lista de pontos da linha em coordenadas de tela.
        :rtype: list
        """
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points

    @property
    def line_points_offset(self):
        """
        Retorna o deslocamento dos pontos da linha em relação ao ponto (0, 0) da tela.

        :return: Deslocamento dos pontos da linha em relação ao ponto (0, 0) da tela.
        :rtype: tuple
        """
        if self._line_points is None:
            self.calc_line_points()
        return self._line_points_offset

    def calc_line_points(self):
        """
        Calcula os pontos da linha em coordenadas de tela.
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
        Invalida os pontos da linha, forçando o recálculo na próxima vez que forem acessados.
        """
        self._line_points = None
        self._line_points_offset = (0, 0)

    def get_x(self, lon):
        """
        Retorna a posição x na tela usando a projeção desta fonte de mapa.
        (0, 0) está localizado no canto superior esquerdo.

        :param lon: Longitude do ponto.
        :type lon: float
        :return: Posição x na tela.
        :rtype: float
        """
        return clamp(lon, MIN_LONGITUDE, MAX_LONGITUDE) * self.ms / 360.0

    def get_y(self, lat):
        """
        Retorna a posição y na tela usando a projeção desta fonte de mapa.
        (0, 0) está localizado no canto superior esquerdo.

        :param lat: Latitude do ponto.
        :type lat: float
        :return: Posição y na tela.
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
        Limpa a linha antiga e desenha a nova linha.
        """
        with self.canvas:
            # Limpa a linha antiga
            self.canvas.clear()

        self._draw_line()

    def _draw_line(self, *args):
        """
        Desenha a linha na tela.
        """
        map_view = self.parent
        self.zoom = map_view.zoom
        self.lon = map_view.lon
        self.lat = map_view.lat

        # Quando o zoom é alterado, devemos desfazer a transformação de dispersão atual
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

            # Desloca pelos pontos da linha
            # (que já foram deslocados para manter as coordenadas mais próximas de zero)
            Translate(*self.line_points_offset)

            Color(*self.color)
            Line(points=self.line_points, width=2)

            # Restaura o contexto do espaço de coordenadas
            PopMatrix()