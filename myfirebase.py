import requests
from kivy.app import App

import requests
from kivy.app import App

class MyFirebase():
    """
    Classe que gerencia a comunicação com o Firebase Authentication e Realtime Database.
    """

    API_KEY = "AIzaSyCL5SzpjM8b1VlO6XSwniNFplITXo99Xmo"

    def criar_conta(self, email, senha):
        """
        Cria uma nova conta de usuário no Firebase Authentication.

        Args:
            email (str): O email do usuário.
            senha (str): A senha do usuário.

        Returns:
            None
        """
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"

        info = {"email": email, 
                "password": senha, 
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print(requisicao_dic)
            # requisicao_dic["idToken"]
            # requisicao_dic["localId"] -> id do usuario
            # requisicao_dic["refreshToken"] -> token que matém o usuário logado
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id # -> coloca o id do usuario no app
            meu_aplicativo.id_token = id_token # -> coloca o token do usuario no app
            
            # salvar o refresh token em um arquivo
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)
            # pegando o valor do id do vendedor para criar a conta com o id
            req_id = requests.get(f"https://aplicativovendashashdojoao-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}")
            id_vendedor = req_id.json()

            link = f"https://aplicativovendashashdojoao-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"

            info_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            
            requests.patch(link, data=info_usuario)
            
            # atualizar o valor do id do vendedor
            proximo_id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f"https://aplicativovendashashdojoao-default-rtdb.firebaseio.com/.json?auth={id_token}", data=info_id_vendedor)


            meu_aplicativo.carregar_info_usuario()
            meu_aplicativo.mudar_tela("homepage")
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def fazer_login(self, email, senha):
        """
        Faz o login do usuário no Firebase Authentication.

        Args:
            email (str): O email do usuário.
            senha (str): A senha do usuário.

        Returns:
            None
        """
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"

        info = {"email": email, 
                "password": senha, 
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print(requisicao_dic)
            # requisicao_dic["idToken"]
            # requisicao_dic["localId"] -> id do usuario
            # requisicao_dic["refreshToken"] -> token que matém o usuário logado
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id # -> coloca o id do usuario no app
            meu_aplicativo.id_token = id_token # -> coloca o token do usuario no app
            
            # salvar o refresh token em um arquivo
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            meu_aplicativo.carregar_info_usuario()
            meu_aplicativo.mudar_tela("homepage")
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        """
        Troca o refresh token por um novo id_token e local_id.

        Args:
            refresh_token (str): O refresh token do usuário.

        Returns:
            tuple: Uma tupla contendo o novo local_id e id_token.
        """
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"
        info = f'{{"grant_type": "refresh_token", "refresh_token": "{refresh_token}"}}'
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        local_id = requisicao_dic["user_id"]
        id_token = requisicao_dic["id_token"]
        return local_id, id_token