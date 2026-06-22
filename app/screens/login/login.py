from kivy.app import App # App é usado para executar e encerrar o programa
from kivy.lang import Builder # Builder é responsável por carregar arquivos .kv manualmente
from pathlib import Path # Path é a forma moderna e multiplataforma de trabalhar com caminhos de arquivos
# Funciona no Windows, Linux, Android (APK) etc.
from kivy.uix.screenmanager import Screen # Screenmanager é usado para gerenciamento de telas
from kivy.animation import Animation # Animation é usado para realizar animações
from kivy.uix.floatlayout import FloatLayout # FloatLayout é usado para administrar os widgets
from kivy.uix.label import Label # Label é usado para criar textos
from kivy.uix.button import Button # Button é usado para criar botões
from kivy.uix.image import Image # Image é usado para adicionar imagens nos layouts e widgets
from kivy.uix.popup import Popup # Popup é usado para mostrar uma mensagem de aviso para o usuario
from kivy.core.window import Window # Window é usado para atribuir funcionalidades ao teclado

from app.core.utils import resource_path # resource_path é um modulo que corrige o caminho relativo dos arquivos usados pelo programa

from app.database.database import banco_de_dados

from app.core.audio.gerenciador_de_audios import falar # função que usa voz para ler o texto

from app.core.state.estado_global import Estado_Global, estado # Função que permite ler e alterar o estado global do audio

from app.core.sessao.gerenciador_sessao import Sessao, sessao # sessao contem a instancia da classe Sessao usada para definir os usuarios logados

# BASE_DIR representa o diretório onde ESTE arquivo .py está localizado
# __file__  -> caminho do arquivo atual
# resolve() -> converte para caminho absoluto real
# parent    -> pega apenas a pasta (diretório pai)
BASE_DIR = Path(__file__).resolve().parent

# Monta o caminho até o arquivo login.kv de forma relativa e segura
# Não usa caminhos absolutos fixos, evitando erros em outros dispositivos
kv_path = BASE_DIR / "login.kv"

# Carrega o arquivo .kv no Kivy
# str() é necessário porque o Builder espera uma string, não um objeto Path
#Builder.load_file(str(kv_path))

Builder.load_file(str(resource_path(kv_path)))
# Carrega o login.kv

class Login(Screen): # Classe Login herda as funcionalidades da classe Screen
	def __init__(self, **kwargs): # Subscreve os parametros  da classe Screen
		super().__init__(**kwargs) # Chama a os parametros da classe Screen e inclui os parametros pasados pelo usuario
		self.id_estado_senha = 0 # Atributo da classe que armazena um valor númerico entre 0 e 1
		self.estado_global = estado # Armazena a instancia do estado global de audio
		self.estado_audio = self.estado_global.get_state # armazena o valor retornado 
		self.novo_estado_audio = self.estado_global
		self.sessao = sessao # Atributo da classe que armazena o usuario logado
		self.botao = self.ids['login'] # Contem a referencia do botao usuario
		falar("Seja bem vindo a ascensão",self.estado_audio()) # Sauda o usuario usando o espeak

	def on_pre_enter(self):
	# Método iniciado antes do layout ser carregado
		Window.bind(on_key_down=self.sair_keyboard) # Lê o teclado e chama o método sair_keyboard quando alguma tecla é pressionada
		self.botao.disabled = False # Habilita o botão de login
		
	def sair_keyboard(self, window, key, *args): 
	# Quando o método é chamado:
		if key == 27: # Verifica se a tecla pressionada foi a tecla ESC no computador ou o botão de voltar no celular
			self.saida() # Chama o método saida que contem um popup e uma animação
			return True # Retorna um valor booleano
	
	def on_pre_leave(self): # Método executadobao sair da tela
		Window.unbind(on_key_down=self.sair_keyboard) # Desvincula o método do teclado
		
	def saida(self): # Essa função mostra um PopUp com animação confirmando se o usuario quer ou não sair do aplicativo
		float = FloatLayout() # Cria um container
		btn1 = Button(text="Sim", pos_hint={"top": 0.70, "right": 0.45}, size_hint=(0.40, 0.40), background_color=(0,0,0,0)) # Confirma que o usuario quer sair
		btn1.bind(on_press=self.sair) # Executa a função sair quando o botão é presionado
		btn1_img = Image(source=str(resource_path("assets/images/imagens/Botao.png")), pos_hint={"top": 0.70, "right": 0.45},size_hint=(0.40, 0.40)) # Adiciona uma imagem de fundo na mesma posição do btn1
		btn2 = Button(text="Não", pos_hint={"top": 0.70, "right": 0.95}, size_hint=(0.40, 0.40), background_color=(0,0,0,0)) # Confirma que o usuario não quer sair
		btn2.bind(on_press=self.voltar) # Conecta o evento de dismiss ao botão btn2
		btn2_img = Image(source=str(resource_path("assets/images/imagens/Botao.png")), pos_hint={"top": 0.70, "right": 0.95}, size_hint=(0.40, 0.40)) # Adiciona uma imagem de fundo na mesma posição btn2
		float.add_widget(btn1_img) # Adiciona a imagem do botão btn1 no layout
		float.add_widget(btn1) # Adiciona o botão Sim no containe
		float.add_widget(btn2_img) # Adiciona a imagem do botão btn2 no layout
		float.add_widget(btn2) # Adiciona o botão Sair no container
		
		self.pop = Popup(title="Você realmente quer sair? ", title_size=(30), title_align=('center'), title_color=(0,1,0,1), content=float, pos_hint={"top":0.63, "right":0.65}, size_hint=(0.30,0.25), background=str(resource_path("assets/images/imagens/aurora.jpg"))) # Cria o Popup
		falar("Você realmente deseja sair?", self.estado_audio()) # usa a voz para perguntar se o usuario realmente deseja sair
		self.pop.open() # Executa o Popup
		
		anim = Animation(pos_hint={"right":0.65}, duration=0.1) + Animation(pos_hint={"right":0.45}, duration=0.1) + Animation(pos_hint={"right": 0.85},duration=0.1) + Animation(pos_hint={"right": 0.65},duration=0.1)# Cria animação
		anim.start(self.pop) # Executa a animação
	
	def sair(self, instance): # Executa a função sair
		App.get_running_app().stop() # Destroi o aplicativo
	
	def voltar(self, instance): # Executa a função Dismiss
		self.pop.dismiss() # Retorna a tela de login
		
	def validar(self): # Executa a função validar
		email = self.ids['email'] # Acessa a entrada de dados que recebe o email do usuario
		email_cadastrado = banco_de_dados.ler_banco_de_dados("app.db", "usuarios", "email_novo",email.text)
		senha_cadastrada = banco_de_dados.ler_banco_de_dados("app.db", "usuarios", "senha", email.text)
		senha = self.ids['senha'] # Acessa a entrada de dados que recebe a senha do usuario
		erro = self.ids['erro'] # Acessa o label que mostra uma mensagem de erro para o usuario
			
		if email.text == "" and senha.text == "": 
		# Se o email e senha estiverem vazios
			erro.text = "Digite seu E-mail e sua senha" 
			# Essa mensagem de erro é mostrada
			falar("Digite seu E-mail e sua senha", self.estado_audio()) # Usa a voz para pedir ao usuario que digite o email e a senha 
			# Notifica o usuario com espeak
		elif email.text == "": 
		# Se o email estiver vazio
			erro.text = "Digite seu E-mail"
			# Essa mensagem de erro aparece
			falar("Digite seu E-mail", self.estado_audio())
			# Notifica o usuario com espeak
		elif "@" not in email.text:
		# Se o email não tiver @
			erro.text = "O E-mail deve conter @"
			# Essa mensagem de erro aparece
			falar("Seu E-mail deve conter @", self.estado_audio())
			# Notifica o usuario com espeak
		elif ".com" not in email.text:
		# Se o email não tiver .com
			erro.text = "O E-mail deve conter .com" 
			# Essa mensagem de erro aparece
			falar("Seu E-mail deve conter .com", self.estado_audio())
			# notifica o usuario com espeak
		elif senha.text == "":
		# Se a senha estiver vazia
			erro.text = "Digite sua senha" 
			# Essa mensagem de erro aparece
			falar("Digite sua senha", self.estado_audio())
		elif len(senha.text) < 6:
		# Se a senha tiver menos de 6 caracteres
			erro.text = "Sua senha deve conter pelo menos 6 caracteres" 
			# Essa mensagem de erro aparece
			falar("Sua senha deve conter pelo menos 6 caracteres", self.estado_audio())
			# Notifica o usuario com espeak
		elif email.text != email_cadastrado: 
		# Se o Email digitado pelo usuario for diferente dos emails cadastrados no banco de dados
			erro.text = "Email não cadastrado"
			# Essa mensagem de erro aparece
			falar("Email não cadastrado", self.estado_audio())
			# Notifica o usuario.com espeak
		elif email.text == email_cadastrado: 
		# Se o email digitado pelo usuario estiver no banco de dados:
			if senha.text != senha_cadastrada:
			# Porém, se a senha estiver errada:
				erro.text = "Senha incorreta"
				# Exibe essa mensagem de erro
				falar("Sua senha está incorreta", self.estado_audio())
				# Notifica o usuario com espeak
			else:
			# Se estiver tudo certo
				self.botao.disabled = True # Desabilita o.botão
				erro.text = "" # Limpa as mensagens de erro
				self.sessao.definir_sessao_atual(email.text) # Define a sessao atual
				email.text = "" # Limpa o campo email
				senha.text = "" # Limpa o campo senha
				return True
		else: 
		# Se não houver erros 
			erro.text = "" 
			# A mensagem de erro desaparece
			
	
	def mostrarsenha(self): 
	# Método que altera o icone e o estado da senha quando chamado
		icone = self.ids["icone_senha"] # Captura as propriedades do icone da entrada de dados que recebe senha
		senha = self.ids["senha"] # Captura as propriedades da entrada de dados que recebe a senha
		
		if self.id_estado_senha == 0: # Se o atributo da classe tiver o valor 0:
			icone.source = str(resource_path("assets/icons/ocultarsenha.png")) # Altera o icone
			senha.password = False # Altera o estado da senha para false
			self.id_estado_senha = 1 # Altera o valor da variavel
		else: # Se o valor for 1:
			icone.source = str(resource_path("assets/icons/mostrarsenha.png")) # Altera o icone
			senha.password = True # Altera o estado da senha para True
			self.id_estado_senha = 0 # Altera o valor da variavel
	
	def alterar_estado(self):
	# Permite alterar o estado global do audio
		estado = self.estado_audio() # acessa o valor do estado global
		print(f"[Login.py] [Line 184] [Estado Global De Audio] {estado}")
		if estado == "0":
		# Se o valor for igual a 0:
			falar("Sistema de áudio desativado", self.estado_audio())
			self.novo_estado_audio.set_state(1) # Altera o valor global para 1
			self.ids["ativar_audio"].source = str(resource_path("assets/icons/desativar_audio.png")) # altera o icone para desativar_audio.png
		else:
		# Se o valor for diferente de 0
			self.novo_estado_audio.set_state(0) # Altera o valor para 0
			self.ids["ativar_audio"].source = str(resource_path("assets/icons/ativar_audio.png")) # altera o icone para ativar_audio.png
			falar("Sistema de áudio ativado", self.estado_audio())
			
			
		
		