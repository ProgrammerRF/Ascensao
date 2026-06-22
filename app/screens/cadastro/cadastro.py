from kivy.uix.screenmanager import Screen # Screenmanager é usado para gerenciamento de telas

from kivy.clock import Clock # Clock é usado para orquestrar os eventos do kivy

from pathlib import Path # Path é a forma moderna e multiplataforma de trabalhar com caminhos de arquivos 

from kivy.lang import Builder # Builder é responsavel por carregar arquivos .kv manualmente

from app.core.audio.gerenciador_de_audios import falar # função que usa voz para ler o texto

from kivy.core.window import Window # Window é usado para atribuir funcionalidades ao teclado

from app.core.utils import resource_path # resource_path é um modulo usado para corrigir o caminho relativo dos arquivos

from app.core.state.estado_global import Estado_Global, estado # Função que permite ler e alterar o estadi global do audio

from app.core.sessao.gerenciador_sessao import Sessao, sessao # contem a instancia da classe Sessao que gerencia os usuarios logados

from app.database.database import banco_de_dados

import traceback

# BASE_DIR representa o diretorio onde este arquivo .py está localizado 
# __file__ caminho do arquivo atual
# resolve() converte para caminho absoluto real
# parent pega apenas a pasta (diretorio pai)

BASE_DIR = Path(__file__).resolve().parent

# Monta o caminho até o arquivo cadastro.kv de forma relativa e segura 
# Não usa caminhos absolutos fixos, evitando erros em outros dispositivos
kv_path = BASE_DIR / "cadastro.kv"

# Carrega o arquivo .kv no kivy
# str() é necessario porque o Builder espera uma string, não um objeto Path

Builder.load_file(str(resource_path(kv_path)))
# Carrega o cadastro.kv 

class Cadastro(Screen): 
	# Cadastro Herda de Screen
	def __init__(self, **kwargs): 
	# __init__ altera os parametros da classe Scree
		super().__init__(**kwargs) 
		# super() Reescreve os parametros da classe e adiciona o novo parametro
		self.id_estado_senha1 = [0] # Atributo da classe que guarda um valor numerico de 0 e 1 usado pela função mostrarsenha1
		self.id_estado_senha2 = [0] # Atributo da classe que guarda um valor numerico de 0 e 1 usado pela função mostrarsenha2
		#self.email = self.ids['email']
		self.estado_global = estado # acessa a instancia global da classe
		self.estado_audio = self.estado_global.get_state # captura o valor do estado global
		self.novo_estado_audio = self.estado_global.set_state # Insere o novo estado global
		self.sessao = sessao # atributo da classe que contem a instancia Sessao
		self.botao = self.ids["cadastrar"] # Contem informações sobre o botão cadastrar

		falar("Para se cadastrar preencha o formulário", self.estado_audio())  # Notifica o usuario o requerimento de preencher os dados do formulario para se cadastrar
		
	def on_pre_enter(self): 
	# Método executado antes de carregar o layout
		Window.bind(on_key_down=self.voltar_keyboard) # Lê o teclado e chama o método voltar_keyboard quando uma tecla é pressionada
		self.botao.disabled = False # Habilita o botão cadastrar assim que o usuario entra na tela

	
	def voltar_keyboard(self, window, key, *args):
	# Quando o método é chamado:
		if key == 27: # Se a tecla pressionada for ESC ou o botão de voltar no android:
			self.manager.current = "login" # Muda para a tela de login
			return True # Retorna um valor booleano
	
	def on_pre_leave(self): 
	# Método executado ao sair da tela
		Window.unbind(on_key_down=self.voltar_keyboard) # Desvicula o método da tecla
		
	def cadastrar(self): 
	# A função cadastrar realiza o cadastro do usuario no sistema
		try:
			email = self.ids['email'] # Captura as informações da entrada de dados email
			print(f"email digitado {email.text}")
			email_cadastrado = banco_de_dados.ler_banco_de_dados(banco="app.db",tabela="usuarios",info="email_novo",email=email.text)
			nome = self.ids['nome']  # Captura as informações da entrada de dados nome
			senha1 = self.ids['senha1'] # Captura as informações da entrada de dados senha1
			senha2 = self.ids['senha2'] # Captura as informações da entrada de dados senha2
			erro = self.ids['erro'] # Captura as informações do texto erro

			print(f"OVER HERE STRANGER.... {email_cadastrado}")
			print(email.text)

			if email.text == email_cadastrado:
				# Se o email digitado já existir no banco de dados
				erro.text = "E-mail já existe no sistema"
				# Exibe essa mensagem de erro
				falar("Seu E-mail já está cadastrado", self.estado_audio())
				# Notifica o usuario com espeak
			elif email.text == "":
				# Se o email estiver vazio
				erro.text = "Digite seu E-mail"
				# Exibe essa mensagem de erro
				falar("Digite seu E-mail", self.estado_audio())
				# Notifica o usuario com espeak
			elif "@" not in email.text:
				# Se o email não tiver @
				erro.text = "O E-mail deve conter @"
				# Exibe essa mensagem de erro
				falar("Seu E-mail deve conter @", self.estado_audio())
				# Notifica o usuario com espeak
			elif ".com" not in email.text:
				# Se o email não tiver .com
				erro.text = "O E-mail deve conter .com"
				# Exibe essa mensagem de erro
				falar("Seu E-mail deve conter .com", self.estado_audio())
				# Notifica o usuario com espeak
			elif " " in email.text:
				erro.text = "O E-mail não pode ter espaços"
				# Exibe a mensagem de erro
				falar("Seu E-mail não pode ter espaços", self.estado_audio())
				# Notifica o usuario com espeak

			elif nome.text == "":
				# Se o nome estiver vazio
				erro.text = "Digite seu nome"
				# Exibe essa mensagem de erro
				falar("Digite seu nome", self.estado_audio())
				# Notifica o usuario usando espeak
			elif senha1.text == "":
				# Se a senha estiver vazia
				erro.text = "Digite sua senha"
				# Exibe essa mensagem de erro
				falar("Digite sua senha", self.estado_audio())
				# Notifica o usuario usando espeak
			elif len(senha1.text) < 6:
				# Se a senha tiver menos que 6 caracteres
				erro.text = "Sua senha deve conter pelo menos 6 caracteres"
				# Exibe essa mensagem de erro
				falar("Sua senha deve conter pelo menos 6 caracteres", self.estado_audio())
				# Notifica o usuario usando espeak
			elif senha2.text == "":
				# Se a senha estiver vazia
				erro.text = "Digite sua senha novamente"
				#Exibe essa mensagem de erro
				falar("Digite sua senha novamente", self.estado_audio())
				# Notifica o usuario usando o espeak
			elif len(senha2.text) < 6:
				# Se a senha tiver menos que 6 caracteres
				erro.text = "Sua senha deve conter pelo menos 6 caracteres"
				# Exibe a mensagem de erro
				falar("Sua senha deve conter pelo menos 6 caracteres", self.estado_audio())
				# Notifica o usuario com espeak
			elif senha1.text != senha2.text:
				# Se as senhas forem diferentes
				erro.text = "As senhas devem ser iguais"
				# Exibe essa mensagem
				falar("As senhas devem ser iguais", self.estado_audio())
				# Notifica o usuario com espeak
			else: # Se todas as condições forem atendidas
				erro.text = "" # o valor do texto fica vazio

				print(email.text)

				banco_de_dados.criar_banco_de_dados("app.db", "usuarios")
				banco_de_dados.inserir_dados_banco_de_dados("app.db", "usuarios", nome.text, email.text, email.text, senha1.text)
				sessao.definir_sessao_atual(email.text)



				# Limpa os campos do formulario
				email.text = ""
				nome.text = ""
				senha1.text = ""
				senha2.text = ""

				# Desabilita o botão de cadastro
				self.botao.disabled = True

				return True
		except Exception as e:
			print(traceback.format_exception(e))
		
	def mostrarsenha1(self): # Função que altera o icone e valor boleano da entrada de dados senha1
		senha1 = self.ids["senha1"] # Armazena os atributos do entrada de dados senha1 
		imagem_senha1 = self.ids["imagem_senha1"] # Armazena os atributos da imagem_senha1
		
		if 0 in self.id_estado_senha1: 
		# Se o valor da variavel id_estado_senha1 for igual a 0:
			imagem_senha1.source=str(resource_path("assets/icons/ocultarsenha.png")) # Muda o icone da entrada de dados
			senha1.password=False # mostra a senha
			self.id_estado_senha1.clear() # Limpa a lista
			self.id_estado_senha1.append(1) # Adiciona o numero 1 a lista
		else: 
		# Se o valor da variavel id_estado_senha1 for igual a 1:
			imagem_senha1.source=str(resource_path("assets/icons/mostrarsenha.png")) # Muda o icone da entrada de dados
			senha1.password=True # Esconde a senha
			self.id_estado_senha1.clear() # Limpa a lista
			self.id_estado_senha1.append(0) # Adiciona o numero 0 a lista
	
	def mostrarsenha2(self):
		# Função que altera o icone e valor boleano da entrada de dados senha2
		senha2 = self.ids["senha2"] # Armazena os atributos do entrada de dados senha2
		imagem_senha2 = self.ids["imagem_senha2"] # Armazena os atributos da imagem_senha2
		
		if 0 in self.id_estado_senha2:
		# Se o valor da variavel id_estado_senha2 for igual a 0:
			imagem_senha2.source=str(resource_path("assets/icons/ocultarsenha.png")) # Muda o icone da entrada de dados
			senha2.password=False # mostra a senha
			self.id_estado_senha2.clear() # Limpa a lista
			self.id_estado_senha2.append(1) # Adiciona o numero 1 a lista
		else: 
		# Se o valor da variavel id_estado_senha2 for igual a 1:
			imagem_senha2.source=str(resource_path("assets/icons/mostrarsenha.png")) # Muda o icone da entrada de dados
			senha2.password=True # Esconde a senha
			self.id_estado_senha2.clear() # Limpa a lista
			self.id_estado_senha2.append(0) # Adiciona o numero 0 a lista
			
	