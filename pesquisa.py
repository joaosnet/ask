from kivy.properties import ListProperty
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest

KV = '''

Screen:
    BoxLayout:
        orientation: 'vertical'
        spacing: 1
        BoxLayout:
            size_hint_y: 1/5
            canvas.before:
                Color:
                    rgba:  0, 0, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size[0], 2
            SearchTextInput:
                id: Search_TextInput_id
                size_hint_y: .97
                pos_hint:{ 'left':0 , 'top': 1}
                hint_text_color: 1,1,1,1
                mode: "fill"
                helper_text_mode: "persistent"
                helper_text: "Search"
                line_color: [1,1,1,1]
                color_normal: [1,1,1,1]

                hint_text: "Partida"
                helper_text: "Informe seu local de Partida"
                helper_text_mode: "on_focus"
                icon_right: "map-marker"
                icon_right_color: app.theme_cls.primary_color
                pos_hint: {'center_x': 0.5,'center_y': 0.5}

                font_size: .35 * self.height
                active_line: False
                multiline: False

        BoxLayout:
            orientation: 'vertical'
            padding: 4
            RecycleView:
                viewclass: 'Search_Select_Option'
                data:app.rv_data
                RecycleBoxLayout:
                    spacing: 15
                    padding : 10
                    default_size: None, None
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: 'vertical'
<Search_Select_Option>:
    on_release: print(self.text)
    IconRightWidget:
        icon: "arrow-top-left"
'''


class Search_Select_Option(OneLineAvatarIconListItem):
    pass


class SearchTextInput(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_list = []

    def on_text(self, instance, value):
        app = MDApp.get_running_app()
        self.get_geocode(value)
        option_list = list(set(self.option_list + value[:value.rfind(' ')].split(' ')))
        val = value[value.rfind(' ') + 1:]
        if not val:
            return
        try:
            app.option_data = []
            for i in range(len(option_list)):
                word = [word for word in option_list if word.startswith(val)][0][len(val):]
                if not word:
                    return
                if self.text + word in option_list:
                    if self.text + word not in app.option_data:
                        popped_suggest = option_list.pop(option_list.index(str(self.text + word)))
                        app.option_data.append(popped_suggest)
                app.update_data(app.option_data)
        except IndexError:
            pass

    def get_geocode(self, adress):

        url = f"https://graphhopper.com/api/1/geocode?q={adress}&point=string&provider=nominatim&limit=5&locale=pt_BR&key=17e8fe9c-35aa-47cb-9c6b-3fbb62b7259b"

        UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error)
    
    def success(self, urlrequest, result):
        print("Success")
        self.option_list = [hit["name"] for hit in result["hits"]]
        print(self.option_list)

    def error(self, urlrequest, result):
        print("error")
        print(result)

    def failure(self, urlrequest, result):
        print("failure")
        print(result)


class HotReload(MDApp):
    rv_data = ListProperty()

    def update_data(self, rv_data_list):
        self.rv_data = [{'text': item} for item in rv_data_list]
        print(self.rv_data, 'update')

    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    HotReload().run() 