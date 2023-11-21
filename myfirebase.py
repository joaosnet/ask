import requests
from kivymd.app import MDApp
from datetime import date

class MyFirebase():
    """
    Classe que gerencia a comunicação com o Firebase Authentication e Realtime Database.
    """

    API_KEY = "AIzaSyCL5SzpjM8b1VlO6XSwniNFplITXo99Xmo"

    # quando clicado confirma a senha e faz o cadastro, quando não, mostra uma mensagem de erro nos campos senha e confirmação de senha
    def confirmar_senha(self, nome, deficiencia, email, senha, confirmacao_senha):
        if senha == confirmacao_senha:
            self.criar_conta(nome, deficiencia, email, senha)
        else:
            meu_aplicativo = MDApp.get_running_app()
            pagina_cadastro = meu_aplicativo.root.get_screen("cadastropage")
            pagina_cadastro.ids["senha_sem_confirmacao"].ids["text_field"].helper_text = "As senhas não coincidem"
            pagina_cadastro.ids["senha_sem_confirmacao"].ids["text_field"].error = True
            pagina_cadastro.ids["senha_de_confirmacao"].ids["text_field"].helper_text = "As senhas não coincidem"
            pagina_cadastro.ids["senha_de_confirmacao"].ids["text_field"].error = True

    def criar_conta(self, nome, deficiencia, email, senha):
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
            # print(requisicao_dic)
            # requisicao_dic["idToken"]
            # requisicao_dic["localId"] -> id do usuario
            # requisicao_dic["refreshToken"] -> token que matém o usuário logado
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = MDApp.get_running_app()
            meu_aplicativo.local_id = local_id # -> coloca o id do usuario no app
            meu_aplicativo.id_token = id_token # -> coloca o token do usuario no app
            
            # salvar o refresh token em um arquivo
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)
            # pegando o valor do id do vendedor para criar a conta com o id
            req_id = requests.get(f"https://inclusiveway-ask-default-rtdb.firebaseio.com/proximo_id.json?auth={id_token}")
            id = req_id.json()

            link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"

            data = date.today().strftime('%d/%m/%Y')

            info_usuario = f'{{"foto_de_perfil": "foto1.png", "nome": "{nome}", "data_criacao_de_conta": "{data}", "deficiencia": "{deficiencia}", "id": "{id}", "telefone": "", "localizacao":""}}'
            
            requests.patch(link, data=info_usuario)
            
            # atualizar o valor do id do vendedor
            proximo_id = int(id) + 1
            info_id_vendedor = f'{{"proximo_id": "{proximo_id}"}}'
            requests.patch(f"https://inclusiveway-ask-default-rtdb.firebaseio.com/.json?auth={id_token}", data=info_id_vendedor)


            meu_aplicativo.carregar_info_usuario()
            meu_aplicativo.mudar_tela("homepage")
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = MDApp.get_running_app()
            pagina_cadastro = meu_aplicativo.root.get_screen("cadastropage")
            if mensagem_erro == "INVALID_EMAIL" or mensagem_erro == "EMAIL_NOT_FOUND":
                pagina_cadastro.ids["email"].helper_text = "Email não cadastrado"
                pagina_cadastro.ids["email"].error = True
            elif mensagem_erro == "EMAIL_EXISTS":
                pagina_cadastro.ids["email"].helper_text = "Email já cadastrado"
                pagina_cadastro.ids["email"].error = True
            elif mensagem_erro == "MISSING_PASSWORD" :
                pagina_cadastro.ids["senha_sem_confirmacao"].ids["text_field"].helper_text = "Faltou a Senha"
                pagina_cadastro.ids["senha_sem_confirmacao"].ids["text_field"].error = True
                pagina_cadastro.ids["senha_de_confirmacao"].ids["text_field"].helper_text = "Faltou a Senha"
                pagina_cadastro.ids["senha_de_confirmacao"].ids["text_field"].error = True
            else:
                pagina_cadastro.ids["mensagem_erro"].text = mensagem_erro
                pagina_cadastro.ids["mensagem_erro"].color = (1, 0, 0, 1)

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
            # print(requisicao_dic)
            # requisicao_dic["idToken"]
            # requisicao_dic["localId"] -> id do usuario
            # requisicao_dic["refreshToken"] -> token que matém o usuário logado
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = MDApp.get_running_app()
            meu_aplicativo.local_id = local_id # -> coloca o id do usuario no app
            meu_aplicativo.id_token = id_token # -> coloca o token do usuario no app
            
            # salvar o refresh token em um arquivo
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)

            meu_aplicativo.carregar_info_usuario()
            meu_aplicativo.mudar_tela("homepage")
        else:
            meu_aplicativo = MDApp.get_running_app()
            mensagem_erro = requisicao_dic["error"]["message"]
            pagina_login = meu_aplicativo.root.get_screen("loginpage")
            if mensagem_erro == "INVALID_EMAIL" or mensagem_erro == "EMAIL_NOT_FOUND":
                pagina_login.ids["email"].helper_text = "Email não cadastrado"
                pagina_login.ids["email"].error = True
            elif mensagem_erro == "INVALID_LOGIN_CREDENTIALS":
                mensagem_erro = "Email e/ou senha incorretos"
                pagina_login.ids["email"].helper_text = mensagem_erro
                pagina_login.ids["email"].error = True
                pagina_login.ids["senha"].ids["text_field"].helper_text = mensagem_erro
                pagina_login.ids["senha"].ids["text_field"].error = True
            elif mensagem_erro == "MISSING_PASSWORD" :
                pagina_login.ids["senha"].ids["text_field"].helper_text = "Faltou a Senha"
                pagina_login.ids["senha"].ids["text_field"].error = True
            else:
                pagina_login.ids["email"].helper_text = mensagem_erro
                pagina_login.ids["email"].error = True

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
    # fazer o logout do app apagando o refresh token do arquivo refresh_token.txt e deixando ele vazio
    def logout(self):
        with open("refresh_token.txt", "w") as f:
            f.write("")
        meu_aplicativo = MDApp.get_running_app()
        meu_aplicativo.local_id = None
        meu_aplicativo.id_token = None
        meu_aplicativo.root.current = "startpage"
        meu_aplicativo.root.transition.direction = "right"

    # lembrar o email e a senha do usuario para fazer o login automaticamente
    def lembrar_senha(self, ativo,email, senha):
        if ativo:
            with open("usuario.txt", "w") as f:
                f.write(f"{email}\n{senha}")
        else:
            with open("usuario.txt", "w") as f:
                f.write("")

    # Função para fazer alterações no perfil do usuario
    def alterar_perfil(self, nome, deficiencia, telefone, localizacao):
        # verificando se algum campo conteve alteração
        if nome != "" and deficiencia != "" and telefone != "" and localizacao != "":
            meu_aplicativo = MDApp.get_running_app()
            id_token = meu_aplicativo.id_token
            local_id = meu_aplicativo.local_id
            link = f"https://inclusiveway-ask-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"
            info = f'{{"nome": "{nome}", "deficiencia": "{deficiencia}", "telefone": "{telefone}", "localizacao": "{localizacao}"}}'
            requisicao = requests.patch(link, data=info)
            requisicao_dic = requisicao.json()
            # atualizar as informações do usuario na homepage
            meu_aplicativo.carregar_info_usuario()
            # escrevendo uma mensagem na tela
            pagina_perfil = meu_aplicativo.root.get_screen("homepage").ids["perfilpage"]
            pagina_perfil.ids["mensagem"].text = "As alterações foram feitas com sucesso"          
        else:
            # escrevendo uma mensagem de erro na tela
            meu_aplicativo = MDApp.get_running_app()
            pagina_perfil = meu_aplicativo.root.get_screen("homepage").ids["perfilpage"]
            pagina_perfil.ids["mensagem"].text = "Nenhuma alteração foi feita, pois algum campo está vazio"