from pathlib import Path
import sqlite3
import traceback
from app.core.utils import resource_path

APP_DIR = Path.home() / "Ascensao"
APP_DIR.mkdir(exist_ok=True)
DATABASE = APP_DIR

class BancoDeDados():
	def __int__(self, **kwargs):
		super().__init__(**kwargs)

	def conectar(self, banco):
		try:
			print((str(resource_path(fr"app\database\{banco}"))))
			return sqlite3.connect((str(resource_path(fr"app\database\{banco}"))))
		except Exception as e:
			print(f"\n[database.py] [BancoDeDados] [conectar] [LINE 13] [ERROR] --> {e}\n")

	def criar_banco_de_dados(self, banco, tabela):
		try:
			con = self.conectar(banco)
			cur = con.cursor()

			cur.execute(f"""
				CREATE TABLE IF NOT EXISTS {tabela} (
					ID INTEGER PRIMARY KEY AUTOINCREMENT,
					NOME TEXT NOT NULL,
					EMAIL_ANTIGO TEXT NOT NULL UNIQUE,
					EMAIL_NOVO TEXT NOT NULL UNIQUE,
					SENHA TEXT NOT NULL
				)
			""")

			con.commit()
			con.close()
		except Exception as e:
			print(f"[database.py] [BancoDeDados] [criar_banco_de_dados] [LINES 19 UNTIL 33] [ERROR] ---> {e}")
		finally:
			con.close()

	def inserir_dados_banco_de_dados(self, banco, tabela, nome, email_antigo, email_novo, senha):
		try:
			con = self.conectar(banco)
			cur = con.cursor()
			cur.execute(f"INSERT INTO {tabela} (nome, email_antigo, email_novo, senha) VALUES (?, ?, ?, ?)", (nome,email_antigo, email_novo, senha,))

			con.commit()
			con.close()
		except Exception as e:
			print(f"[database.py] [BancoDeDados] [inserir_dados_banco_de_dados] [LINES 39 UNTIL 44] [ERROR] ---> {e}")

	def atualizar_email(self, banco, tabela,email_antigo, email_novo_antigo, email_novo):
		try:
			con = self.conectar(banco)
			cur = con.cursor()
			cur.execute(f"UPDATE {tabela} SET EMAIL_NOVO = (?) WHERE EMAIL_ANTIGO = (?)", (email_novo, email_antigo,))
			cur.execute(f"UPDATE {tabela} SET EMAIL_ANTIGO = (?) WHERE EMAIL_ANTIGO = (?)", (email_novo_antigo, email_antigo,))
			con.commit()
		except Exception as e:
			print(f"[database.py] [BancoDeDados] [inserir_dados_banco_de_dados] [LINES 52 UNTIL 56] [ERROR] ---> {e}")
		finally:
			con.close()

	def atualizar_nome(self, banco, tabela, email_novo, nome_novo):
		try:
			con = self.conectar(banco)
			cur = con.cursor()
			cur.execute(f"UPDATE {tabela} SET NOME = (?) WHERE EMAIL_NOVO = (?)", (nome_novo, email_novo,))
			con.commit()
		except Exception as e:
			print(f"[database.py] [BancoDeDados] [inserir_dados_banco_de_dados] [LINES 64 UNTIL 67] [ERROR] ---> {e}")
		finally:
			con.close()

	def atualizar_senha(self, banco, tabela, email_novo, senha_nova):
		try:
			con = self.conectar(banco)
			cur = con.cursor()
			cur.execute(f"UPDATE {tabela} SET SENHA = (?) WHERE EMAIL_NOVO = (?)",(senha_nova, email_novo,))
			con.commit()
		except Exception as e:
			print(f"[database.py] [BancoDeDados] [inserir_dados_banco_de_dados] [LINES 75 UNTIL 78] [ERROR] ---> {e}")
		finally:
			con.close()


	def ler_banco_de_dados(self, banco, tabela, info, email=""):
		try:
			con = self.conectar(banco)
			cur = con.cursor()
			cur.execute(f"SELECT * FROM {tabela}")

			linhas = cur.fetchall()

			if info == "*":
				return linhas

			elif info == "email_antigo":
				cur.execute(f"SELECT * FROM {tabela} WHERE EMAIL_NOVO == (?)", (email,))
				emails_antigos = cur.fetchall()
				for email_antigo in emails_antigos:
					return email_antigo[2]

			elif info == "email_novo":
				cur.execute(f"SELECT * FROM {tabela} WHERE EMAIL_NOVO == (?)", (email,))
				emails_novos = cur.fetchall()
				print(emails_novos)
				for email_novo in emails_novos:
					return email_novo[3]

			elif info == "nome":
				cur.execute(f"SELECT * FROM {tabela} WHERE EMAIL_NOVO == (?)",(email,))
				nomes = cur.fetchall()
				for nome in nomes:
					print(nome[1])
					return nome[1]

			elif info == "senha":
				cur.execute(f"SELECT * FROM {tabela} WHERE EMAIL_NOVO == (?)", (email,))
				senhas = cur.fetchall()
				for senha in senhas:
					print(senha[4])
					return senha[4]

		except TypeError as e:
			print(f"[database.py] [BancoDeDados] [ler_banco_de_dados] [LINES 50 UNTIL 68] [ERROR] --> {e}")
		except sqlite3.OperationalError as e:
			print(f"[database.py] [BancoDeDados] [ler_banco_de_dados] [LINES 87 UNTIL 120] [ERROR] --> {e}")
			self.criar_banco_de_dados("app.db", "usuarios")
		except ValueError as e:
			print(traceback.format_exception(e))
		finally:
			con.close()


banco_de_dados = BancoDeDados()
#banco_de_dados.criar_banco_de_dados("app.db", "usuarios")
#banco_de_dados.inserir_dados_banco_de_dados("app.db","usuarios","Rafael", "rafael@gmail.com","rafael?@gmail.com","123456")
#usuarios = banco_de_dados.ler_banco_de_dados("app.db", "usuarios")