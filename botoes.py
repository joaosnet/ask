from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class ImageButton(ButtonBehavior, Image):
    pass

class LabelButton(ButtonBehavior, Label):
    pass