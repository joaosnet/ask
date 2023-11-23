from kivymd.app import MDApp
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog


class GpsHelper():
    """
    Classe responsável por gerenciar o GPS do dispositivo móvel e atualizar a posição do GpsBlinker.
    """
    has_centered_map = False

    def run(self):
        """
        Inicia o gerenciamento do GPS e atualiza a posição do GpsBlinker.
        """
        # Obtendo o GpsBlinker da tela
        gps_blinker = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["blinker"]
        gps_blinker2 = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage2"].ids["blinker"]
        # Iniciando o pulso do GpsBlinker
        gps_blinker.blink()
        gps_blinker2.blink()
    

        # Requisita permissão de GPS no Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            # Iniciando o gerenciamento do GPS
            def callback(permission, results):
                if all([res for res in results]):
                    from plyer import gps
                    gps.configure(on_location=self.update_blinker_position,
                                on_status=self.on_auth_status)
                    gps.start(minTime=100, minDistance=1)
                else:
                    print("Permissão de GPS negada")
            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                Permission.ACCESS_FINE_LOCATION], callback)

        # Configura o GPS no iOS
        if platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position,
                          on_status=self.on_auth_status)
            gps.start(minTime=500, minDistance=0)


    def update_blinker_position(self, *args, **kwargs):
        """
        Atualiza a posição do GpsBlinker com base na posição atual do GPS.
        """
        self.my_lat = kwargs['lat']
        self.my_lon = kwargs['lon']
        # Atualiza a posição do GpsBlinker
        gps_blinker = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["blinker"]
        gps_blinker2 = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage2"].ids["blinker"]
        gps_blinker.lat = self.my_lat
        gps_blinker.lon = self.my_lon
        gps_blinker2.lat = self.my_lat
        gps_blinker2.lon = self.my_lon

        # Centraliza o mapa na posição atual do GPS
        if not self.has_centered_map:
            map = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["mapview"]
            map2 = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage2"].ids["mapview"]
            map.center_on(self.my_lat, self.my_lon)
            map2.center_on(self.my_lat, self.my_lon)
            self.has_centered_map = True


    def on_auth_status(self, general_status, status_message):
        """
        Verifica o status de autorização do GPS e exibe um popup de erro caso necessário.
        """
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    # funcao que retorna a latitude e longitude
    def get_lat_lon(self):
        """
        Retorna a latitude e longitude da posição atual do GPS.
        """
        return self.my_lat, self.my_lon

    def open_gps_access_popup(self):
        """
        Exibe um popup de erro informando que o acesso ao GPS precisa ser habilitado.
        """
        dialog = MDDialog(title="Erro no GPS", text="Você precisa habilitar o acesso ao GPS para o aplicativo funcionar corretamente")
        dialog.open()