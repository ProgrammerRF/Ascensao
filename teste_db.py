from kivy.core.audio import SoundLoader
import time
import subprocess
from pathlib import Path
import traceback

APP = Path.home() / "Ascensao"
APP.mkdir(exist_ok=True)

def threading_falar(texto, estado):
	try:
		if estado == "0":
			pass
		else:
			subprocess.run([
				fr"{APP}\bin\piper\piper.exe",
				"--model",
				fr"{APP}\bin\piper\pt_BR-cadu-medium.onnx",
				"--output_file",
				fr"{APP}\assets\audio\voices\audio.wav"
			], input=texto, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)

			sound = SoundLoader.load(fr"{APP}\assets\audio\voices\audio.wav")

			if sound:
				sound.play()
	except Exception as e:
		print(f"[Gerenciador_de_audios] [Erro] {traceback.format_exception(e)} [Linha] 17\n")


texto = "ASCENSAO TESTE"
print(texto.capitalize())
