from kivy.properties import ListProperty
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.list import TwoLineRightIconListItem
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from pprint import pprint as pp
from threading import Thread

# Exemplo
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

#Opção de Seleção de Pesquisa
<Search_Select_Option>:
    on_release: 
        app.root.ids.Search_TextInput_id.text = self.text
    IconRightWidget:
        icon: "arrow-top-left"
'''


class Search_Select_Option(TwoLineRightIconListItem):
    pass


class SearchTextInput(MDTextField):
    """
    Classe que representa um campo de texto para pesquisa.

    Herda da classe MDTextField.

    Atributos:
        error (bool): Indica se ocorreu um erro durante a pesquisa.
        option_list (list): Lista de opções de pesquisa.

    Métodos:
        on_text(self, instance, value): Método chamado quando o texto do campo é alterado.
        get_geocode(self, adress): Obtém as coordenadas geográficas de um endereço usando a API do GraphHopper.
        success(self, urlrequest, result): Função de retorno de chamada para o caso de sucesso da solicitação da API.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error = False
        self.option_list = []

    def on_text(self, instance, value):
        """
        Método chamado quando o texto do campo é alterado.

        Args:
            instance: Instância do campo de texto.
            value: Novo valor do texto.

        Returns:
            None
        """
        Thread(target=self.get_geocode, args=(value,)).start()

    def get_geocode(self, adress):
        """
        Obtém as coordenadas geográficas de um endereço usando a API do GraphHopper.

        Args:
            adress (str): O endereço a ser pesquisado.

        Returns:
            None
        """
        # trocando espaços por +
        adress = adress.replace(" ", "+")

        url = f"https://graphhopper.com/api/1/geocode?q={adress}&point=string&provider=nominatim&limit=30&locale=en&key=17e8fe9c-35aa-47cb-9c6b-3fbb62b7259b"

        UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error)

    def success(self, urlrequest, result):
        """
        Função de retorno de chamada para o caso de sucesso da solicitação da API.

        Args:
            urlrequest: A solicitação da API.
            result: O resultado da solicitação da API.

        Returns:
            None
        """
        self.option_list = [(hit["name"], hit["point"]) for hit in result["hits"]]

        # Obter a instância do aplicativo em execução
        app = MDApp.get_running_app()

        # Atualizar a lista de opções do aplicativo
        app.option_data = self.option_list

        # Atualizar a lista de sugestões na interface do usuário
        app.update_data(app.option_data)

    def error(self, urlrequest, result):
        """
        Função de retorno de chamada para o caso de erro na solicitação da API.

        Args:
            urlrequest: A solicitação da API.
            result: O resultado da solicitação da API.

        Returns:
            None
        """
        print("error")
        print(result)

    def failure(self, urlrequest, result):
        """
        Função de retorno de chamada para o caso de falha na solicitação da API.

        Args:
            urlrequest: A solicitação da API.
            result: O resultado da solicitação da API.

        Returns:
            None
        """
        print("failure")
        print(result)

class HotReload(MDApp):
    """
    Classe principal para o aplicativo HotReload.
    """

    rv_data = ListProperty()
    """
    Lista de propriedades para armazenar os dados da RecyclerView.
    """

    def update_data(self, rv_data_list):
        """
        Atualiza os dados da RecyclerView com uma nova lista de dados.

        Args:
            rv_data_list (list): Lista de dados para atualizar a RecyclerView.
        """
        self.rv_data = [{'text': item[0], "secondary_text": f"{item[1]['lat']}, {item[1]['lng']}"} for item in rv_data_list]
        print(self.rv_data, 'update')

    def build(self):
        """
        Constrói a interface do aplicativo.

        Returns:
            Widget: A interface do aplicativo construída.
        """
        return Builder.load_string(KV)

if __name__ == "__main__":
    HotReload().run() 