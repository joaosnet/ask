from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class ImageButton(ButtonBehavior, Image):
    pass