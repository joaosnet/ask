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
        # Get a reference to GpsBlinker, then call blink()
        gps_blinker = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["blinker"]
        # Start blinking the GpsBlinker
        gps_blinker.blink()

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    MDApp.mostrar_alerta("Permissão de GPS Concedida", "Você precisa habilitar o acesso ao GPS para o aplicativo funcionar corretamente")
                    try:
                        from plyer import gps
                        gps.configure(on_location=self.update_blinker_position,
                                    on_status=self.on_auth_status)
                        gps.start(minTime=1000, minDistance=0)
                    except Exception as e:
                        MDApp.mostrar_alerta("Erro ao Iniciar o GPS", "Ocorreu um erro ao iniciar o GPS: " + str(e))
                else:
                    MDApp.mostrar_alerta("Permissão de GPS Não Concedida", "Você precisa habilitar o acesso ao GPS para o aplicativo funcionar corretamente")  

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)
            
            

        # Configure GPS
        if platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position,
                          on_status=self.on_auth_status)
            gps.start(minTime=1000, minDistance=0)


    def update_blinker_position(self, *args, **kwargs):
        """
        Atualiza a posição do GpsBlinker com base na posição atual do GPS.
        """
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        # MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["erro"].text = "GPS POSITION", my_lat, my_lon
        # Update GpsBlinker position
        gps_blinker = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["blinker"]
        gps_blinker.lat = my_lat
        gps_blinker.lon = my_lon

        MDApp.mostrar_alerta("Posição do GPS", str(my_lat) + ", " + str(my_lon))

        # Centraliza o mapa na posição atual do GPS
        if not self.has_centered_map:
            map = MDApp.get_running_app().root.get_screen("homepage").ids["mapapage1"].ids["mapview"]
            map.center_on(my_lat, my_lon)
            self.has_centered_map = True


    def on_auth_status(self, general_status, status_message):
        """
        Verifica o status de autorização do GPS e exibe um popup de erro caso necessário.
        """
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        """
        Exibe um popup de erro informando que o acesso ao GPS precisa ser habilitado.
        """
        dialog = MDDialog(title="Erro no GPS", text="Você precisa habilitar o acesso ao GPS para o aplicativo funcionar corretamente")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()