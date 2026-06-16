from kivy.uix.label import Label # Permite adicionar Textos na tela
from kivy.uix.button import Button # Permite criar botões 
from kivy.uix.image import Image # Permite criar imagens
from kivy.uix.popup import Popup # Permite criar notificações personalizadas
from kivy.uix.floatlayout import FloatLayout # Cria um layout
from app.core.utils import resource_path # Corrige os caminhos relativos
from kivy.clock import Clock # Clock é usado para orquestrar os eventos do kivy

class Avisos(): # Notifica o usuario sobre a sincronização do firebase
	def __init__(self, **kwargs): # Passa os parametros a classe
		super().__init__(**kwargs) # Adiciona os parametros a classe
		
	def desconectado(self): # Notifica o usuario quando o cadastro é feito desconectado
		aviso = Label(text="As informações serão sincronizadas ao firebase\nassim que a conexão for reestabelecida", pos_hint={"top": 1.10, "right":1}) #Mensagem
		texto_botao = Label(text="Entendi", pos_hint={"top":0.30, "right":0.70}, size_hint=(0.40,0.40)) # Texto do botão 
		botao = Button(pos_hint={"top":0.30, "right":0.70}, size_hint=(0.40,0.40), background_color=(0,0,0,0)) # Botão invisivel
		botao.bind(on_press=self.entendido) # Conecta o evento self.entendido ao botão
		icone_botao = Image(source=str(resource_path("assets/images/imagens/Botao.png")), pos_hint={"top":0.30,"right":0.70}, size_hint=(0.40,0.40)) # Adiciona o icone do botão na mesma posição
		imagem_de_fundo = str(resource_path("assets/images/imagens/aurora.jpg")) # Imagem de fundo
		box = FloatLayout(pos_hint={"top":1, "right":1}) # Layout que contem os widgets
		
		box.add_widget(aviso) # Adiciona a mensagem
		box.add_widget(botao) # Adiciona o botão 
		box.add_widget(icone_botao) # Adiciona o icone do botão
		box.add_widget(texto_botao) # Adiciona o texto do botão
		
		self.pop = Popup(title="AVISO".center(80), content=box, pos_hint={"top": 0.65, "right":0.90}, size_hint=(0.80,0.20), background=imagem_de_fundo) # Cria o popup
		self.pop.open() # Abre o popup
		Clock.schedule_once(lambda dt: self.pop.dismiss(), 4) # Dispensa o popup após 4 segundos
	
	def conectado(self): # Notifica o usuario quando a conexão é reestabelecida
		aviso = Label(text="As informações foram sincronizadas \ne enviadas ao firebase", pos_hint={"top": 1.10, "right":1}) # Mensagem
		texto_botao = Label(text="Entendi", pos_hint={"top":0.30, "right":0.70}, size_hint=(0.40,0.40)) # Texto do botão 
		botao = Button(pos_hint={"top":0.30, "right":0.70}, size_hint=(0.40,0.40), background_color=(0,0,0,0)) #Botão invisivel 
		botao.bind(on_press=self.entendido) # Conecta o botão ao evento self.entendido
		icone_botao = Image(source=str(resource_path("assets/images/imagens/Botao.png")), pos_hint={"top":0.30,"right":0.70}, size_hint=(0.40,0.40)) # Adiciona o icone na mesma posição do botão
		imagem_de_fundo = str(resource_path("assets/images/imagens/aurora.jpg")) # Adiciona a imagem de fundo
		box = FloatLayout(pos_hint={"top":1, "right":1}) # Cria o layout
		
		box.add_widget(aviso) # Adiciona a mensagem ao layout
		box.add_widget(botao) # Adiciona o botão ao layout
		box.add_widget(icone_botao) # Adiciona o icone ao layout
		box.add_widget(texto_botao) # Adiciona o texto ao layout
		
		self.pop = Popup(title="AVISO".center(80), content=box, pos_hint={"top": 0.65, "right":0.90}, size_hint=(0.80,0.20), background=imagem_de_fundo) # Cria o popup
		self.pop.open() # Abre o popup
		Clock.schedule_once(lambda dt: self.pop.dismiss(), 4) # Dispensa o popup após 4 segundos
		
	def dados_alterados(self): # Notifica o usuario quando a conexão é reestabelecida
		aviso = Label(text="Informações alteradas com sucesso", pos_hint={"top": 1.10, "right":1})
		# Mensagem
		texto_botao = Label(text="Entendi", pos_hint={"top":0.30, "right":0.70}, size_hint=(0.40,0.40)) # Texto do botão 
		botao = Button(pos_hint={"top":0.30, "right":0.70}, size_hint=(0.40,0.40), background_color=(0,0,0,0)) #Botão invisivel 
		botao.bind(on_press=self.entendido) # Conecta o botão ao evento self.entendido
		icone_botao = Image(source=str(resource_path("assets/images/imagens/Botao.png")), pos_hint={"top":0.30,"right":0.70}, size_hint=(0.40,0.40)) # Adiciona o icone na mesma posição do botão
		imagem_de_fundo = str(resource_path("assets/images/imagens/aurora.jpg")) # Adiciona a imagem de fundo
		box = FloatLayout(pos_hint={"top":1, "right":1}) # Cria o layout
		
		box.add_widget(aviso) # Adiciona a mensagem ao layout
		box.add_widget(botao) # Adiciona o botão ao layout
		box.add_widget(icone_botao) # Adiciona o icone ao layout
		box.add_widget(texto_botao) # Adiciona o texto ao layout
		
		self.pop = Popup(title="AVISO".center(80), content=box, pos_hint={"top": 0.65, "right":0.90}, size_hint=(0.80,0.20), background=imagem_de_fundo) # Cria o popup
		self.pop.open() # Abre o popup
		Clock.schedule_once(lambda dt: self.pop.dismiss(), 4) # Dispensa o popup após 4 segundos
	
	def entendido(self, instance): # Encerra a mensagem
		self.pop.dismiss() # Fecha o popup

avisos = Avisos() # Instancia da classe