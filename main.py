#!/user/bin/env python
# -*- coding: utf8 -*-
#qpy:3
#qpy:kivy

__name__ # reservado
APP_NAME = "Ascensão"

__Author__ = "Rafael Moraes De Oliveira"
__Date__ = "Quinta-Feira (22/01/2026)"
__Version__ = "Alpha"

from kivy.app import App # App é usado para criação e execução do aplicativo
from app.screens.login import login # importa o conteudo do arquivo login.py
from app.screens.cadastro import cadastro # importa o conteudo do arquivo cadastro.py
from app.screens.principal import principal # Importa a tela principal
from app.screens.configuracao import configuracao # Importa a tela de configurações
from app.screens.alterar_dados import alterar_dados
# Importa a tela de alterar dados cadatrais
from kivy.clock import Clock # Clock é usado para oruqestrar eventos
from kivy.uix.screenmanager import ScreenManager # Screenmanager é usado para gerenciamento de telas
from kivy.lang import Builder # Builder é usado para acessar o conteudo de arquivos.kv
from app.core.utils import resource_path # resource_path é usado para correção de caminhos relativos usados pelo programa

sm = ScreenManager()
class Ascensao(App): # Herda as funcionalidades da superclasse App
	
	def on_start(self):
		self.alterar_tela("login")

	def rp(self, path): 
	# método que permite usar o resource_path no arquivo.kv
		return str(resource_path(path))
		# Retorna o caminho como string)()

	def alterar_tela(self, tela):
		if tela == "login":
			if sm.has_screen(tela):
				sm.current = "login"
			else:
				sm.add_widget(login.Login(name="login"))
				sm.current = "login"

		elif tela == "cadastro":
			if sm.has_screen(tela):
				sm.current = "cadastro"
			else:
				sm.add_widget(cadastro.Cadastro(name="cadastro"))
				sm.current = "cadastro"
		elif tela == "principal":
			if sm.has_screen(tela):
				sm.current = "principal"
			else:
				sm.add_widget(principal.Principal(name="principal"))
				sm.current = "principal"
		elif tela == "configuracao":
			if sm.has_screen(tela):
				sm.current = "configuracao"
			else:
				sm.add_widget(configuracao.Configuracao(name="configuracao"))
				sm.current = "configuracao"
		elif tela == "alterar_dados":
			if sm.has_screen(tela):
				sm.current = "alterar_dados"
			else:
				sm.add_widget(alterar_dados.Alterar_Dados(name="alterar_dados"))
				sm.current = "alterar_dados"
		else:
			pass

	def build(self): # Método construtor
		return sm # retorna o objeto ScreenManager
			
if __name__ == '__main__': # Executa o aplicativo somente se for o arquivo principal
	Ascensao().run() # Inicia o aplicativo
