from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivy.properties import OptionProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class TextoMenu1(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class TextoMenu2(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class ImageButton(ButtonBehavior, Image):
    pass
#  Recriando o botão de obstáculo para que ele fique na lateral direita
class ObstaculoButton(MDFloatingActionButtonSpeedDial):
    """
    Classe que representa um botão de obstáculo.

    Possui métodos para definir a posição dos rótulos flutuantes,
    do botão raiz e dos botões inferiores em uma pilha.
    """

    anchor = OptionProperty('right', option=["right", "left"])

    def set_pos_labels(self, widget):
        """
        Define a posição dos rótulos flutuantes.

        :param widget: O widget dos rótulos flutuantes.
        """

        if self.anchor == "right":
            widget.x = Window.width - widget.width - dp(86)
        elif self.anchor == "left":
            widget.x = widget.width + dp(86)

    def set_pos_root_button(self, instance):
        """
        Define a posição do botão raiz.

        :param instance: A instância do botão raiz.
        """

        if self.anchor == "right":
            instance.y = dp(20)
            instance.x = Window.width - (dp(56) + dp(20))
        elif self.anchor == "left":
            instance.y = dp(20)
            instance.x = (dp(56) + dp(20))

    def set_pos_bottom_buttons(self, instance):
        """
        Define a posição dos botões inferiores em uma pilha.

        :param instance: A instância dos botões inferiores.
        """

        if self.anchor == "right":
            if self.state != "open":
                instance.y = instance.height / 2
            instance.x = Window.width - (instance.height + instance.width / 2)
        elif self.anchor == "left":
            if self.state != "open":
                instance.y = instance.height / 2
            instance.x = (instance.height + instance.width / 2)