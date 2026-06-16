class Sessao(): # Define a sessão atual 
	def __init__(self): 
		self.sessao = [0] # atributo da classe que contem o usuario logado
	
	def ver_sessao_atual(self): # Permite ver qual usuario está logado
		sessao_atual = str(self.sessao) # Armazena a sessao atual como string
		return sessao_atual.replace("[","").replace("]","").replace("'","") # Retorna o valor formatado removendo colchetes e aspas
		
	def definir_sessao_atual(self, email): # Define o usuario logado
		self.sessao.clear() # Limpa a sessão anterior
		self.sessao.append(email) # Adiciona o novo usuario a sessão
		return self.sessao # Retorna o atributo da classe
		
	def logoff(self): # Encerra a sessão atual
		self.sessao.clear() # Limpa o atributo da classe

sessao = Sessao() # Instancia da classe