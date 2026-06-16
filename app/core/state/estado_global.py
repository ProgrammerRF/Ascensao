class Estado_Global():
# Classe que possui o estado global do audio
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.estado_audio = [0]
	
	def get_state(self):
	# captura o estado global e retorna o valor do atributo self.estado_audio
		estado_atual = str(self.estado_audio)
		estado_atual_formatado = self.replace_method(estado_atual)
		return estado_atual_formatado
	
	def set_state(self, valor):
	# Altera o valor do atributo self.estado_audio
		self.estado_audio.clear()
		self.estado_audio.append(valor)
	
	def replace_method(self, valor):
	# Remove o [] da lista
		return valor.replace("[","").replace("]","")
		
# Instancia a classe
estado = Estado_Global()
