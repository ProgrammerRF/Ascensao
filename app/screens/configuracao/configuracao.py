from kivy.uix.screenmanager import Screen # Screen é usado para definir as telas do ScreenManager
from pathlib import Path # Path é usado para definir caminhos relativos
from app.core.utils import resource_path # resource_path é usado para corrigir caminhos relativos
from app.core.sessao.gerenciador_sessao import sessao # sessão contêm a instancia da classe Sessao
from kivy.clock import Clock # Clock é usado para gerenciar os eventos do kivy
from kivy.core.window import Window # Window é usado para alterar as funcionalidades das teclas do teclado
from kivy.lang import Builder # Builder é usado para acessar o conteudo do arquivo.kv
from app.core.audio.gerenciador_de_audios import falar
from app.core.state.estado_global import estado
import os

DIR_SCREENS = Path(__file__).resolve().parent.parent # Acessa o diretorio screens
DIR_KV = DIR_SCREENS / "configuracao" / "configuracao.kv" # acessa o arquivo configurações.kv

Builder.load_file(str(resource_path(DIR_KV))) # Carrega o conteudo da tela configurações.kv

class Configuracao(Screen): # Herda Screen
	def __init__(self, **kwargs): # Altera os parametros da superclasse
		super().__init__(**kwargs) # Adiciona os da superclasse e os novos parametros passados
		self.estado_audio_global = estado.get_state

	def on_pre_enter(self): # Ao entrar na tela:
		Window.bind(on_key_down=self.keyboard) # Altera a funcionalidade da tecla 27
		
	def on_pre_leave(self): # Ao sair da tela
		Window.unbind(on_key_down=self.keyboard) # Desvincula a tecla 27 da função keyboard
	
	def keyboard(self, window, key, *args): # Altera a funcionalidade da tecla 27, fazendo o app retornar para a tela anterior quando a tecla é pressionada
		if key == 27: # Se a tecla 27 for pressionada:
			self.manager.current = "principal" # Volta para a tela principal
		return True # Retorna um valor booleano verdadeiro
	
	





