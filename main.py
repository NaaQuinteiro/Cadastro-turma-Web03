import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib


# Criação de Classe com artificio de HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
    
        try:
            
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                content = f.read()
                self.wfile.write(content.encode('utf-8'))
                f.close
                return None
            
        except FileNotFoundError:
            print("Page is not fond")

        return super().list_directory(path)
    

    def do_GET(self):

        # Rota login
        if self.path == '/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()# le o contedo do arquivo login 
                
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8')) # escreve o conteudo da página
            # Caso dê erro
            except FileNotFoundError:
                self.send_error(404, "File not found")
        
        elif self.path == '/login_failed':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
            

                mensagem = 'Login e/ou senha incorretos. Tente novamente'
                content = content.replace('<!--Mensagem de erro inserida aqui-->', 
                                          f'<div class="error-message">{mensagem}</div>' )

            #Envia o conteudo modificado para o cliente 
            self.wfile.write(content.encode('utf-8')) 

        elif self.path.startswith('/cadastro'):
                query_params = parse_qs(urlparse(self.path).query)
                login = query_params.get('login', [''])[0]
                senha = query_params.get('senha', [''])[0]


                welcome_message= f'Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu Cadastro.'

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                    content=cadastro_file.read()
                
                content = content.replace('{login}', login)
                content = content.replace('{senha}', senha)
                content = content.replace('{welcome_message}', welcome_message)

                self.wfile.write(content.encode('utf-8'))

                return

        elif self.path.startswith('/cadastrar_turma'):
             self.send_response(200)
             self.send_header("content-type", "text/html; charset=utf-8")
             self.end_headers()

             with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as file:
                content = file.read()
                
                self.wfile.write(content.encode('utf-8'))
                
                return
        
        elif self.path.startswith('/cadastrar_atividade'):
             self.send_response(200)
             self.send_header("content-type", "text/html; charset=utf-8")
             self.end_headers()

             with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as file:
                content = file.read()
                
                self.wfile.write(content.encode('utf-8'))
                
                return

        else:

            super().do_GET()

    def usuario_existente(self, login, senha):

            with open('dados.login.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
                        if login == stored_login:

                            senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
                            print('usuário existente')
                            print("cheguei aqui significando que localizei o login informado")
                            print("senha: " + senha)
                            print(" senha_armazenada: " + senha)
                            print(stored_senha_hash)
                            return senha_hash == stored_senha_hash
            return False
    
    def turma_existente(self, cod_turma, descricao):
        # Vericação se a turma já existe 
        with open('dados_turma.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_cod, stored_descricao = line.strip().split(";")

                    if cod_turma == stored_cod or descricao == stored_descricao:
                        return True
        return False
    
    def atividade_existente(self, cod_atividade, descricao):
        # Vericação se a turma já existe 
        with open('dados_atividade.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_cod, stored_descricao = line.strip().split(";")

                    if cod_atividade == stored_cod or descricao == stored_descricao:
                        return True
        return False
    
    def adicionar_usuario(self, login, senha, nome):
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        with open('dados.login.txt', 'a', encoding='utf-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')

    def adicionar_turma(self, cod_turma, descricao):
        with open('dados_turma.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cod_turma};{descricao}\n')

    def adicionar_atividade(self, cod_atividade, descricao):
        with open('dados_atividade.txt', 'a', encoding='utf-8') as file:
            file.write(f'{cod_atividade};{descricao}\n')
    
    def remover_ultima_linha(self, arquivo):
        print('Vou excluir a última linha')
        with open(arquivo, 'r', encoding='urf-8') as file:
            lines =file.readlines()
        with open (arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])

    
    def do_POST(self):
        #verifica se a rota é "/enviar_login" (isso tem que estar no action do formulario )
        if self.path == '/enviar_login':
            content_length = int(self.headers['Content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')

            form_data = parse_qs(body, keep_blank_values=True)

            print("Dados Formulário:")
            print("Email:", form_data.get('email', [''][0]))
            print("Senha:", form_data.get('senha', [''][0]))

            login = form_data.get('email',[''])[0]
            senha = form_data.get('senha',[''])[0]

            if self.usuario_existente(login, senha):

                with open(os.path.join(os.getcwd(), 'page_professor.html'), 'r', encoding='utf-8') as page_professor_file:
                    content = page_professor_file.read() # le o contedo do arquivo login 

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            else:

                if any(line.startswith(f'{login};') for line in open('dados.login.txt', 'r', encoding='utf-8')):

                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return 

                else:
                    #Armazena os dados num arquivo txt
                    # with open('dados.login.txt', 'a', encoding='utf-8') as file:
                        # login = form_data.get('email', [''])[0]
                        # senha = form_data.get('senha', [''])[0]
                        # file.write(f'{login};{senha};' + 'none' + '\n')

                        #redirecionando o cliente para a rota /cadastro com os dados de login e senha 
                        self.adicionar_usuario(login, senha, nome='None')
                        self.send_response(302)
                        self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                        self.end_headers()
                        return

        elif self.path.startswith('/confirmar_cadastro'):

            content_length= int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data=parse_qs(body, keep_blank_values=True)

            login = form_data.get('login', [''])[0]
            senha = form_data.get('senha', [''])[0]
            nome = form_data.get('nome', [''])[0]

            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
            print('nome: ' + nome)

            if self.usuario_existente(login, senha):
                with open ('dados.login.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                with open ('dados.login.txt', 'w', encoding='utf-8') as file:
                    for line in lines:
                        stored_login, stored_senha, stored_nome = line.strip().split(';')
                        if login == stored_login and senha_hash == stored_senha:
                            line = f'{login};{senha_hash};{nome}\n'
                        file.write(line)

                self.send_response(302)
                self.send_header('Location', '/page_professor.html')
                # self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
            
            else:
                self.remover_ultima_linha('dados.login.txt')
                self.send_response(302)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('A senha não confere. Retome o procedimento!'.encode('utf-8'))
            
        elif self.path.startswith('/cadastrar_turma'):
            content_length =  int(self.headers['content-length'])

            body= self.rfile.read(content_length).decode('utf-8')

            from_data = parse_qs(body, keep_blank_values=True)

            cod_turma = from_data.get('codigo-turma', [''])[0]
            descricao = from_data.get('descricao', [''])[0]

            if cod_turma.strip()== '' or descricao.strip() == '':
                
                mensagem_erro = "Os campos não foram preenchidos corretamente, tente novamente."
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_turma.html', 'r', encoding='utf-8') as file:
                    content = file.read()

                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')

                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
            
            elif self.turma_existente(cod_turma, descricao) == True:
                # self.send_response(302)  
                # self.send_header("Location", "/cadastro_turma_failed")
                # self.end_headers
                # self.send_response(302)
                # self.send_header("Content-type", "text/html; charset=utf-8")
                # self.end_headers()
                # self.wfile.write("Turma já cadastrada, tente novamente com outros dados.".encode('utf-8'))
                
                mensagem_erro = "Turma já cadastrada, tente novamente com outros dados."
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_turma.html', 'r', encoding='utf-8') as file:
                    content = file.read()

                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')

                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
            
            else:
                # Se os campos estiverem preenchidos, adiciona a turma
                self.adicionar_turma(cod_turma, descricao)

                # self.send_response(302)
                # self.send_header("Location", "/cadastrar_turma")
                # self.end_headers()

                mensagem_erro = "Turma cadastrada com sucesso!"
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_turma.html', 'r', encoding='utf-8') as file:
                    content = file.read()

                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')

                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))

        elif self.path.startswith('/cadastrar_atividade'):
            content_length =  int(self.headers['content-length'])

            body= self.rfile.read(content_length).decode('utf-8')

            from_data = parse_qs(body, keep_blank_values=True)

            cod_atividade= from_data.get('codigo-atividade', [''])[0]
            descricao = from_data.get('descricao', [''])[0]

            if cod_atividade.strip()== '' or descricao.strip() == '':
                
                # self.send_response(302)
                # self.send_header('Location', '/cadastro_turma_failed')
                # self.end_headers()
                # self.send_response(302)
                # self.send_header("Content-type", "text/html; charset=utf-8")
                # self.end_headers()
                # self.wfile.write("Os campos não foram preenchidos corretamente, tente novamente.".encode('utf-8'))

                mensagem_erro = "Os campos não foram preenchidos corretamente, tente novamente!"
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_atividade.html', 'r', encoding='utf-8') as file:
                    content = file.read()

                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')

                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))

                

            
            elif self.atividade_existente(cod_atividade, descricao) == True:
                # self.send_response(302)  
                # self.send_header("Location", "/cadastro_turma_failed")
                # self.end_headers
                # self.send_response(302)
                # self.send_header("Content-type", "text/html; charset=utf-8")
                # self.end_headers()
                # self.wfile.write("Atividade já cadastrada, tente novamente com outros dados.".encode('utf-8'))
                mensagem_erro = "Atividade já cadastrada, tente novamente com outros dados."
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_atividade.html', 'r', encoding='utf-8') as file:
                    content = file.read()

                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')

                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))
            
            else:
                # Se os campos estiverem preenchidos, adiciona a turma
                self.adicionar_atividade(cod_atividade, descricao)

                # self.send_response(302)
                # self.send_header("Location", "/cadastrar_atividade")
                # self.end_headers()

                
                mensagem_erro = "Atividade cadastrada com sucesso!"
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()

                # Ler o conteúdo original do arquivo ou variável
                with open('cadastro_atividade.html', 'r', encoding='utf-8') as file:
                    content = file.read()

                # Substituir o marcador pela mensagem de erro
                content = content.replace('<!--Mensagem de erro inserida aqui-->', f'<div class="error-message">{mensagem_erro}</div>')

                # Enviar a resposta com o conteúdo modificado
                self.wfile.write(content.encode('utf-8'))

        else:
            #Se não for a rota definifa, conrinua com o comportamento padrão
            super(MyHandler, self).do_POST()

endereco_ip = "0.0.0.0"
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()