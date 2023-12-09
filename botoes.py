from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivy.properties import OptionProperty

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

class ObstaculoButton(MDFloatingActionButtonSpeedDial):
    anchor = OptionProperty("right", option=["right"])