from kivy.uix.screenmanager import Screen # Screen define as telas do screenmanager
from kivy.core.window import Window # Window é usado para alterar funcionalidades do teclado
from kivy.lang import Builder # Builder é usado para carregar o conteudo doa arquivos.kv
from pathlib import Path # Path é usado para acessar caminhos relativos
from app.core.utils import resource_path # resource_path é usado para corrigir caminhos relativos
from app.core.sessao.gerenciador_sessao import sessao # sessao contêm a instancia da classe Sessao usada para gerenciar a sessao atual do usuario logado
from app.core.state.estado_global import estado # estado contêm a instancia da classe Estado_Global usada para gerenciar o estado global de audio
from app.core.audio.gerenciador_de_audios import falar # falar é usado para notificar o usuario por voz com o espeak
from kivy.clock import Clock # Clock é usado para orquestrar os eventos do kivy
from app.database.database import banco_de_dados

PATH_DIR = Path(__file__).resolve().parent.parent # Acessa o diretorio Screens
DIR_KV = str(PATH_DIR / "alterar_dados") # Acessa o diretorio alterar_dados

GUI = Builder.load_file(DIR_KV + "/alterar_dados.kv") # Carrega o conteudo do alterar_dados.kv

class Alterar_Dados(Screen): # Atualiza os dados dos usuarios cadastrados no SQL e no Firebase
	def __init__(self, **kwargs): # Altera os parâmetros da superclasse Screen
		super().__init__(**kwargs) # Chama os parametros originais da superclasse e inclui os novos parametros passados
		
		# Atributo da classe que:
		self.mostrar_ocultar_senha = [0] # Armazena valores numericos (0 e 1) 
		self.nome_antigo = None # Armazena o nome antigo do usuario cadastrado
		self.email_novo = None
		self.email_antigo = None # Armazena o email antigo do usuario
		self.senha_antiga = None # Armazena a senha antiga do usuario
		self.botao = self.ids['botao'] # Armazena o indice do botão alterar dados cadastrais
		self.estado_audio_global = estado.get_state # Armazena o estado global de audio
		
	def on_pre_enter(self): # Ao entrar na tela:
		Window.bind(on_key_down=self.keyboard) # Vincula o teclado a função keyboard
		usuario_logado = sessao.ver_sessao_atual()
		self.email_antigo = banco_de_dados.ler_banco_de_dados("app.db","usuarios", "email_antigo", usuario_logado)
		self.ids["email_antigo"].text = self.email_antigo
		self.email_novo = banco_de_dados.ler_banco_de_dados("app.db","usuarios", "email_novo", usuario_logado)
		self.ids["email_novo"].text = self.email_novo
		self.nome_antigo = banco_de_dados.ler_banco_de_dados("app.db", "usuarios", "nome", usuario_logado)
		self.ids["nome"].text = self.nome_antigo
		self.senha_antiga = banco_de_dados.ler_banco_de_dados("app.db", "usuarios", "senha", usuario_logado)
		self.ids["senha"].text = self.senha_antiga
		self.botao.disabled = False # Habilita o botão alterar dados cadastrais


		
	def on_pre_leave(self): # Ao sair da tela:
		Window.unbind(on_key_down=self.keyboard) # Desvincula o evento keyboard do teclado
	
	def keyboard(self, window, key, *args): # Altera a funacionalidade da tecla 27
		if key == 27: # Se a tecla 27 for pressionada:
			self.manager.current = "configuracao" # Volta para a tela de confugurações
			return True # Retorna um valor booleano verdadeiro
		else: # Se a tecla não for pressionada: 
			pass # Continua a execução (esse else é muito importante, sem ele todas as teclas perdem a funcionalidade e não será possivel alterar os campos da tela alterar dados)
	
	def mostrar_senha(self): # Altera o valor booleano do atributo password da entrada de dadoa senha e o icone de mostrar/ocultar senha
		senha = self.ids["senha"] # Armazena o id da entrada de dados senha
		icone = self.ids["icone"] # Armazena o id do icone mostrar/ocultar senha
		estado = str(self.mostrar_ocultar_senha) # Converte para string o valor numerico (entre 0 e 1) armazenado no atributo da classe (self.mostrar_ocultar_senha)
		estado_formatado = estado.replace("[","").replace("]","").replace("'","") # Remove colchetes e aspas
		
		if estado_formatado == "0": # Se o valor numerico do atributo da classe for 0:
			senha.password = False # Altera o valor booleano da senha para False (mostrando a senha)
			icone.source = str(resource_path("assets/icons/ocultarsenha.png")) # Converte para string o caminho relativo corrigido e altera o icone mostarsenha.png para o icone ocultarsenha.png 
			self.mostrar_ocultar_senha.clear() # Limpa a lista
			self.mostrar_ocultar_senha.append(1) # Adiciona o valor numerico 1 a lista
		else: # Se o valor numerico do atributo for diferente de 0:
			icone.source = str(resource_path("assets/icons/mostrarsenha.png")) # Converte para string o caminho relativo corrigido e altera o icone ocultarsenha.png para mostrarsenha.png
			senha.password = True # Altera o valor booleano do atributo password da senha para True (ocultando a senha)
			self.mostrar_ocultar_senha.clear() # Limpa a lista
			self.mostrar_ocultar_senha.append(0) # Adiciona o valor numerico 0 na lista
	
	def validar(self): # Valida as informações passadas nas entradas de dados e atualiza se tudo estiver correto
		nome_novo = self.ids["nome"] # Armazena o id da entrada de dados nome
		email_novo = self.ids["email_novo"] # Armazena o id da entrada de dados email
		senha_nova = self.ids["senha"] # Armazena o id da entrada de dados senha
		erro = self.ids["erro"] # armazena o id do label erro
		
		if email_novo.text.lower() == "" and nome_novo.text.capitalize() == "" and senha_nova.text == "": # Se todos os campos estiverem vazios:
			erro.text = "Preencha os campos do formulário" # Mostrar essa mensagem de erro
			falar("Preencha os campos do formulário", self.estado_audio_global()) # Notifica o usuario por voz usando espeak
		elif email_novo.text.lower() == "": # Se o campo email estiver vazio:
			erro.text = "Digite seu email" # Mostra uma mensagem de erro
			falar("Digite seu email", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif "@" not in email_novo.text.lower(): # Se o campo email não tiver @:
			erro.text = "Seu email deve conter @" # Mostrar uma mensagem de erro
			falar("Seu email deve conter @", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif ".com" not in email_novo.text.lower(): # Se o campo email não tiver .com:
			erro.text = "Seu email deve conter .com" # Mostrar uma mensagem de erro
			falar("Seu email deve conter .com", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif " " in email_novo.text.lower(): # Se o campo email tiver espaços:
			erro.text = "Seu email não pode conter espaços" # Mostra uma mensagem de erro
			falar("Seu email não pode conter espaços", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif nome_novo.text.capitalize() == "": # Se o campo nome estiver vazio:
			erro.text = "Digite seu nome" # Mostra uma mensagem de erro
			falar("Digite seu nome", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif " " in nome_novo.text.capitalize(): # Se houver espaços no nome:
			erro.text = "Seu nome não pode conter espaços" # Mostra uma mensagem de erro
			falar("Seu nome não pode conter espaços", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif senha_nova.text == "": # Se o campo senha estiver vazio:
			erro.text = "Digite sua senha" # Mostra uma mensagem de erro
			falar("Digite sua senha", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		elif " " in senha_nova.text: # Se o campo de senha tiver espaços:
			erro.text = "Sua senha não pode conter espaços" # Mostra uma mensagem de erro
			falar("Sua senha não pode conter espaços", self.estado_audio_global())
		elif len(senha_nova.text) < 6: # Se o tamanho da senha for menor que 6 caracteres:
			erro.text = "Sua senha deve ter pelo menos 6 digitos" # Mostra uma mensagem de erro
			falar("Sua senha deve ter pelo menos 6 digitos", self.estado_audio_global()) # Notifica o usuario por voz usando o espeak
		else: # Se não houverem erros:
			erro.text = "" # Apaga a mensagem de erro
			if email_novo.text.lower() == self.email_novo and nome_novo.text.capitalize() == self.nome_antigo and senha_nova.text == self.senha_antiga:
				pass
			else:
				self.sincronia_atualizacao()
				return True
	
	def sincronia_atualizacao(self): # Atualiza os dados no SQL e firebase de acordo com o estado de conetividade do usuario
		nome_novo = self.ids["nome"] # Armazena o id da entrada de dados nome
		email_novo = self.ids["email_novo"] # Armazena o id da entrada de dados email
		senha_nova = self.ids["senha"] # Armazena o id da entrada de dados senha

		if email_novo.text.lower() == self.email_novo:
			pass
		else:
			banco_de_dados.atualizar_email("app.db", "usuarios", self.email_antigo, self.email_novo, email_novo.text.lower())

		if nome_novo.text.capitalize() == self.nome_antigo:
			pass
		else:
			banco_de_dados.atualizar_nome("app.db", "usuarios", self.email_novo, nome_novo.text.capitalize())

		if senha_nova.text == self.senha_antiga:
			pass
		else:
			banco_de_dados.atualizar_senha("app.db", "usuarios", self.email_novo, senha_nova.text)


		#banco_de_dados.atualizar_banco_de_dados("app.db", "usuarios", self.email_antigo, self.email_novo, email_novo.text, self.nome_antigo, nome_novo.text, self.senha_antiga, senha_nova.text)

		sessao.definir_sessao_atual(email_novo.text.lower()) # Define a sessao atual passando o novo email
					
		self.botao.disabled = True # Desabilita o botão
		falar("Dados alterados com sucesso", self.estado_audio_global())
