import subprocess # subprocess permite que o python execute programas do sistema operacional
from app.core.utils import resource_path
import threading

def falar(texto, estado):
	threading.Thread(target=threading_falar, args=(texto, estado), daemon=True).start()

def threading_falar(texto, estado):
	try: # Caso ocorra algum erro, continua a execução
		if estado == "1": # Se o valor passado como parametro for 1:
			pass # Continua executando
		else: # Se o valor for diferente:
			subprocess.run([
			str(resource_path("bin/espeak/espeak.exe")), # Programa executado
			"-v", "pt-br", # Linguagem
			"-s", "135", # Velocidade
			"-p","55", # Tom
			"-a", "180", # Amplitude
			texto
			],
			creationflags=subprocess.CREATE_NO_WINDOW) # Gera uma voz que fala o texto passado como parametro
	except Exception as e: # Se o espeak não existir:
		print(f"[Gerenciador_de_audios] [Erro] {e} [Linha] 17\n") # Mostra essa mensagem de erro
