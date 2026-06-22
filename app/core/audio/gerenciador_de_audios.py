import subprocess # subprocess permite que o python execute programas do sistema operacional
from app.core.utils import resource_path
import threading
import traceback
from kivy.core.audio import SoundLoader
import time

def falar(texto, estado):
	threading.Thread(target=threading_falar, args=(texto, estado), daemon=True).start()

def threading_falar_espeak(texto, estado):
	try: # Caso ocorra algum erro, continua a execução
		if estado == "1": # Se o valor passado como parametro for 1:
			pass # Continua executando
		else: # Se o valor for diferente:
			subprocess.run([
			str(resource_path("bin/espeak/espeak.exe")), # Programa executado
			"-v", "pt-br", # Linguagem
			"-s", "150", # Velocidade
			"-p","48", # Tom
			"-g", "0", # pausa
			"-a", "170", # Amplitude
			texto
			],
			creationflags=subprocess.CREATE_NO_WINDOW) # Gera uma voz que fala o texto passado como parametro
	except Exception as e: # Se o espeak não existir:
		print(f"[Gerenciador_de_audios] [Erro] {e} [Linha] 17\n") # Mostra essa mensagem de erro,,


def threading_falar(texto, estado):
	try:
		if estado == "1":
			pass
		else:
			subprocess.run([
				str(resource_path(r"bin\piper\piper.exe")),
				"--model",
				str(resource_path(r"bin\piper\pt_BR-cadu-medium.onnx")),
				"--output_file",
				str(resource_path(r"assets\audio\voices\audio.wav"))
			], input=texto, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

			sound = SoundLoader.load(str(resource_path(r"assets\audio\voices\audio.wav")))

			if sound:
				sound.play()
				time.sleep(sound.length)
	except Exception as e:
		print(f"[Gerenciador_de_audios] [Erro] {traceback.format_exception(e)} [Linha] 17\n")


