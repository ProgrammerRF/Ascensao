from kivy.uix.screenmanager import Screen # Screen é usado para definir as telas adicionadas ao ScreenManager
from kivy.lang import Builder # Builder é usado para carregar os arquivos .kv
from kivy.uix.button import Button # Button é usado para criar botões
from kivy.uix.image import Image # Image é usado para adicionar imagens 
from kivy.uix.popup import Popup # Popup é usado para criar mensagens personalizadas e interativas
from kivy.uix.floatlayout import FloatLayout # FloatLayout é usado para organizar os widgets dentro de um layout
from kivy.animation import Animation # Animation é usado para criar animações
from pathlib import Path # Path é usado para configurar caminhos relativos
from app.core.audio.gerenciador_de_audios import falar # falar é uma função do modulo gerenciador_de_audios usada para transmitir as mensagens para o usuario usando o espeak
from app.core.state.estado_global import Estado_Global, estado # estado contem a instancia da classe Estado_Global e é usada para gerenciar o estado global do audio
from app.core.sessao.gerenciador_sessao import Sessao, sessao # sessao contem a instancia da classe Sessao usada para gerenciar os usuarios logados no sistema
from app.core.utils import resource_path # resource_path é usado para corrigir os caminhos relativos facilitando na geração de arquivos executaveis
from kivy.core.window import Window # Window é usada para ler e gerenciar as funcionalidades do teclado
from kivy.clock import Clock # Clock é usada para gerenciar a ordem do eventos no kivy
from config.secrets import API_KEY
from app.database.database import banco_de_dados
from kivy.graphics import Color, RoundedRectangle
from openai import OpenAI
import threading
import unicodedata

BASE_DIR = Path(__file__).resolve().parent # localiza a baze screens
kv_dir = BASE_DIR / "principal.kv" # acesso o caminho do arquivo principal.kv de forma relativa

Builder.load_file(str(resource_path(kv_dir))) # Carrega o arquivo principal.kv usando o resource_path para corrigir o caminho

openai = OpenAI(api_key=API_KEY)

class Principal(Screen): # Principal herda da superclasse Screen
	def __init__(self, **kwargs): # altera os parametros da superclasse Screen
		super().__init__(**kwargs) # Adiciona os parametros passados e adiciona aos parametros da superclasse Screen
		self.estado_audio = estado.get_state # Atributo da classe que contem a variavel estado da classe Estado_Global
		self.sessao = sessao # atributo da classe que armazena a variavel sessao da classe Sessao
		self.usuario_logado = self.ids["usuario"]

		email_usuario = sessao.ver_sessao_atual()
		nome_usuario = str(banco_de_dados.ler_banco_de_dados("app.db", "usuarios", "nome", email_usuario))
		print(nome_usuario)
		self.usuario_logado.text = nome_usuario
		falar(f"Olá, {nome_usuario}. Como posso te ajudar hoje?", self.estado_audio())


	def on_pre_enter(self): # Ao entrar na tela:
		Window.bind(on_key_down=self.keyboard) # chama a função keyboard que altera a funcionalidade da tecla 27
		email_usuario = sessao.ver_sessao_atual()
		nome_usuario = banco_de_dados.ler_banco_de_dados("app.db", "usuarios", "nome", email_usuario)
		self.usuario_logado.text = nome_usuario

		# ===== Aviso ===== 
		# O código abaixo está no on_press temporariamente para adaptar o texto do zen do python que aparece na tela principal, porém quando movida para outra funçã especifica quando a inteligencia artificial estiver sendo desenvolvida 
		
		Clock.schedule_once(lambda dt: self.ids['resposta_ia'].texture_update(), 0.1) # Atualiza a textura do texto gerado pela inteligencia artificial
		Clock.schedule_once(
				lambda dt: setattr(
					self.ids['resposta_ia'],
					'height',
					self.ids['resposta_ia'].texture_size[1] + 50 # Espaço extra
				), 0.15
				) # Organiza de forma automatica o texto para ficar legivel
	
	def on_pre_leave(self): # Quando o usuario sai da tela
		Window.unbind(on_key_down=self.keyboard) # A função keyboard é desvinculada da tecla 27 
		#sessao.logoff()
		
	def keyboard(self, window, key, *args): # Altera a funcionalidade da tecla 27
		if key == 27: # Se a tecla 27 for pressionada
			self.saida() # Chama a função saida
			return True # retorna um valor booleano verdadeiro
		else:
			pass
	
	def saida(self): # Essa função mostra um PopUp com animação confirmando se o usuario quer ou não sair do aplicativo
		float = FloatLayout() # Cria um container
		btn1 = Button(pos_hint={"top": 0.70, "right": 0.45}, size_hint=(0.40, 0.40), background_color=(0,0,0,0)) # Confirma que o usuario quer sair
		btn1.bind(on_press=self.sair) # Executa a função sair quando o botão é presionado
		btn1_img = Image(source=str(resource_path("assets/images/imagens/btns.png")), pos_hint={"top": 0.70, "right": 0.45},size_hint=(0.40, 0.40)) # Adiciona uma imagem de fundo na mesma posição do btn1
		btn2 = Button(pos_hint={"top": 0.70, "right": 0.95}, size_hint=(0.40, 0.40), background_color=(0,0,0,0)) # Confirma que o usuario não quer sair
		btn2.bind(on_press=self.voltar) # Conecta o evento de dismiss ao botão btn2
		btn2_img = Image(source=str(resource_path("assets/images/imagens/btnn.png")), pos_hint={"top": 0.70, "right": 0.95}, size_hint=(0.40, 0.40)) # Adiciona uma imagem de fundo na mesma posição btn2
		float.add_widget(btn1_img) # Adiciona a imagem do botão btn1 no layout
		float.add_widget(btn1) # Adiciona o botão Sim no containe
		float.add_widget(btn2_img) # Adiciona a imagem do botão btn2 no layout
		float.add_widget(btn2) # Adiciona o botão Sair no container
		
		self.pop = Popup(title="Você realmente quer sair? ", title_size=(25), title_align=('center'), title_color=(1,1,1,1), content=float, pos_hint={"top":0.65, "right":0.65}, size_hint=(0.30,0.25), background=str(resource_path("assets/images/imagens/aurora4.png"))) # Cria o Popup
		falar("Você realmente deseja sair?", self.estado_audio())
		self.pop.open() # Executa o Popup
		
		anim = Animation(pos_hint={"right":0.65}, duration=0.1) + Animation(pos_hint={"right":0.45}, duration=0.1) + Animation(pos_hint={"right": 0.85},duration=0.1) + Animation(pos_hint={"right": 0.65}, duration=0.1)# Cria animação
		anim.start(self.pop) # Executa a animação
	
	def sair(self, instance): # Executa a função sair
		self.pop.dismiss() # Fecha o popup
		self.sessao.logoff() # Encerra a sessão
		self.manager.current = "login" # Encerra a seção e volta para a tela de login
	
	def voltar(self, instance): # Executa a função Dismiss
		self.pop.dismiss() # Retorna a tela de login
	
	def alterar_posicao(self): # Altera a posição da entrada de dados do usuario, está sendo usada apenas como testes no android, porém será desabilitada no desktop
		entrada = self.ids["pergunta"] # Contem a referencia da entrada de dados pergunta
		
		if entrada.focus: # Se a entrada de dados for pressionada:
			entrada.pos_hint = {"top": 0.48} # altera a altura 
		else: # se outra parte da tela for pressionada
			entrada.pos_hint = {"top": 0.18} # Retorna para a altura original

	def resposta_ia(self):
		threading.Thread(target=self.resposta_ia_thread, daemon=True).start()

	def resposta_ia_thread(self):
		pergunta_id = self.ids["pergunta"]
		pergunta = str(pergunta_id.text)
		resposta = self.ids["resposta_ia"]
		botao = self.ids["btn_enviar"]

		Clock.schedule_once(self.limpar_campo)

		botao.disabled = True
		response = openai.responses.create(
			model="gpt-5",
			input=pergunta
		)

		texto = unicodedata.normalize("NFKD", response.output_text)
		falar(texto, self.estado_audio())
		resposta.text = response.output_text

		botao.disabled = False

		Clock.schedule_once(lambda dt: self.ids['resposta_ia'].texture_update(),
							0.1)  # Atualiza a textura do texto gerado pela inteligencia artificial
		Clock.schedule_once(
			lambda dt: setattr(
				self.ids['resposta_ia'],
				'height',
				self.ids['resposta_ia'].texture_size[1] + 50  # Espaço extra
			), 0.15
		)  # Organiza de forma automatica o texto para ficar legive

	def limpar_campo(self, instance):
		pergunta = self.ids["pergunta"]
		pergunta.text = ""
		self.sombreamento()

	def sombreamento(self):
		indice_sombra = self.ids["float"]
		sombra = RoundedButton(
		text="",
		pos_hint={"top": 0.40, "right": 1},
		size_hint=(1, 0.15))

		indice_sombra.add_widget(sombra)






class RoundedButton(Button):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.background_color = (0,0,0,0)

		with self.canvas.before:
			Color(0,0,0,0.8)
			self.rect = RoundedRectangle(
				radius=[50],
				pos=self.pos,
				size=self.size
			)
			self.bind(pos=self.update_rect, size=self.update_rect)

	def update_rect(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size



