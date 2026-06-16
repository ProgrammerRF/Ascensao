from kivy.clock import Clock # Clock é usado para gerenciar os eventos do kivy
from app.core.conectividade.popups import avisos # avisos contem a instancia da classe Avisos
from app.database import database # database é usado para gerenciar os bancos de dados, na atualização irei adicionar apenas base para não ter que chamar database.base no código
import requests # usado para requisições de rede

class Internet(): # Monitora e analisa a conectividade do usuario
	def __init__(self, **kwargs): # passa parametros a classe
		super().__init__(**kwargs) # Adiciona os novos parametros a classe
		self.estado = [""] # Atributo da classe que contem o estado de conectividade
		self.estado_formatado = str(self.estado).replace("[","").replace("]","").replace("'","") # Formata o estado da classe removendo colchetes e aspas
		self.loop = None # atributo da classe alterado conforme o loop é ou não executado
		
	def verificar_internet(self,estado, email_antigo="", email_novo="", nome_antigo="", nome_novo="", senha_antiga="", senha_nova=""): #Verifica o estado de conectividade e inicia ou encerra o loop
		if estado == True: # Se o usuario estiver desconectado
			self.loop = Clock.schedule_interval(self.conectividade, 15) # inicia o loop de verificação a cada 15 segundos
			print("[CLOCK] [STATUS] LOOP INICIADO")
		else:# Se o usuario estiver conectado:
			estado_global = str(self.estado)
			estado_global_formatado = estado_global.replace("[","").replace("]","").replace("'","")
			
			if estado_global_formatado == "Conectado":
				if self.loop: # Se estiver em loop:
					self.loop.cancel() # Encerra o loop
					
			database.base.conectado("", email_antigo, email_novo, nome_antigo, nome_novo, senha_antiga, senha_nova) # Envia as informações para o firebase e limpa a tabela sincronia
			self.conectividade("") # Verifica novamente a conectividade e atualiza o atributo da classe
	
	def conectividade(self, dt): # Verifica a conectividade e atualiza o atributo da classe
		try: # Tratamento de excessões
			requests.get("https://www.google.com/", timeout=3) # Tenta acessar o site do google
			self.estado.clear() #limpa o estado anterior
			self.estado.append("Conectado") # Adiciona o novo estado
			
		except: # Se o usuario estiver desconectado
			self.estado.clear() # Limpa o estado anterior
			self.estado.append("Desconectado") # Adiciona o novo estado
	
	def verificar_estado(self): # Verifica o estado atual
		estado = str(self.estado).replace("[","").replace("]","").replace("'","") # armazena o estado como string
		return estado # retorna o estado atual

internet = Internet() # Instancia da classe
