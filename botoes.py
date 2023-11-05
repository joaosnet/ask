from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()