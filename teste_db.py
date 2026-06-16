from pathlib import Path
import os
import sqlite3
from app.database.database import banco_de_dados

DIR_PATH = Path(__file__).resolve().parent
NEW_DIR = str(DIR_PATH / "app" / "database")

def conectar():
	return sqlite3.connect(NEW_DIR + "/" + "emails_antigos.db")
	
def criar_usuario():
	con = conectar()
	cur = con.cursor()
	
	cur.execute("""
CREATE TABLE IF NOT EXISTS emails (
	email_antigo TEXT NOT NULL,
	email_novo TEXT NOT NULL
)
""")
	
	con.commit()
	con.close()

def inserir_dados(email_antigo, email_novo):
	con = conectar()
	cur = con.cursor()
	
	cur.execute("INSERT INTO emails (email_antigo, email_novo) VALUES (?,?)", (email_antigo, email_novo))
	
	con.commit()
	con.close()
	
def ler_dados_emails_antigos(email_antigo):
	con = conectar()
	cur = con.cursor()
	
	cur.execute("SELECT email_antigo FROM emails WHERE email_antigo = (?)",(email_antigo))
	
	emails_antigos = cur.fetchall()
	
	con.close()
	
	return emails_antigos

def ler_dados_emails_novos():
	con = conectar()
	cur = con.cursor()
	
	cur.execute("SELECT email_novo FROM emails WHERE email_novo = (?)", ("rafaelml@gmail.com",))
	
	emails_novos = cur.fetchall()
	
	for novos in emails_novos:
		print(novos)
	
	con.close()
	
	return emails_novos

#base.novo("app.db","usuarios")
#base.novo("sincronia.db","sincronia")
#base.novo("atualizacao.db","atualizacao")

info = banco_de_dados.ler_banco_de_dados('app.db','usuarios', info="*")
print(info)