from kivy_garden.mapview import MapMarker
from kivy.animation import Animation


class GpsBlinker(MapMarker):
    """Classe que representa um marcador de mapa que pisca.

    Essa classe herda da classe MapMarker e adiciona a funcionalidade de piscar.
    """

    def blink(self):
        # Animation that changes the blink size and opacity
        anim = Animation(outer_opacity=0, blink_size=50)
        # When the animation completes, reset the animation, then repeat
        anim.bind(on_complete=self.reset)
        anim.start(self)


    def reset(self, *args):
        self.outer_opacity = 1
        self.blink_size = self.default_blink_size
        self.blink()
