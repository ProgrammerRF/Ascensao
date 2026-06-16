import sys # sys modulo de sistema
from pathlib import Path # Path permite definir caminhos relativos

def resource_path(relative_path: str) -> str:
	"""
	Retorna o caminho correto tanto no modo normal quanto no executável do pyinstaller
	"""
	if hasattr(sys, "_MEIPASS"):
		return (Path(sys._MEIPASS) / relative_path)
	
	# Raiz do projeto (main.py)
	base_path = Path(__file__).resolve().parents[2]
	return str(base_path /relative_path)
