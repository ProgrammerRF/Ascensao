import threading
import traceback
import sqlite3
import sys

from pathlib import Path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.clock import Clock


# ============================================================
# LOCALIZAÇÃO DOS ARQUIVOS
# ============================================================

# __file__ representa o arquivo monitor_de_rede.py.
#
# Exemplo:
#
# C:\Ascensao\app\screens\monitor_de_rede\monitor_de_rede.py
#
CURRENT_DIR = Path(__file__).resolve().parent


# ============================================================
# ARQUIVO KV
# ============================================================

# O arquivo monitor_de_rede.kv está na mesma pasta
# do monitor_de_rede.py.
#
# Usamos str() para entregar uma string ao Kivy.

MONITOR_DE_REDE_KV = str(
    CURRENT_DIR / "monitor_de_rede.kv"
)


# ============================================================
# LOCALIZAÇÃO DO DIRETÓRIO APP
# ============================================================

if getattr(sys, "frozen", False):

    # --------------------------------------------------------
    # PYINSTALLER
    # --------------------------------------------------------
    #
    # Estamos executando o .exe.
    #
    # Como o PyInstaller foi configurado com:
    #
    # --add-data "app\database\dominios.db;app\database"
    #
    # o banco ficará dentro de:
    #
    # _MEIPASS\app\database\dominios.db
    #
    # Portanto começamos pelo _MEIPASS e entramos em "app".
    # --------------------------------------------------------

    APP_DIR = Path(sys._MEIPASS) / "app"

else:

    # --------------------------------------------------------
    # PYCHARM
    # --------------------------------------------------------
    #
    # Estrutura:
    #
    # Ascensao
    # └── app
    # └── screens
    # └── monitor_de_rede
    # └── monitor_de_rede.py
    #
    # CURRENT_DIR:
    #
    # app\screens\monitor_de_rede
    #
    # CURRENT_DIR.parent:
    #
    # app\screens
    #
    # CURRENT_DIR.parent.parent:
    #
    # app
    # --------------------------------------------------------

    APP_DIR = CURRENT_DIR.parent.parent


# ============================================================
# BANCO DE DADOS
# ============================================================

# Agora APP_DIR aponta para:
#
# PyCharm:
# C:\Ascensao\app
#
# PyInstaller:
# _MEIPASS\app
#
# Então os dois cenários usam a mesma estrutura interna.

HOSTS_TXT = str(
    APP_DIR / "database" / "dominios.db"
)


# ============================================================
# DIAGNÓSTICO
# ============================================================

print(
    f"[MonitorDeRede] KV: {MONITOR_DE_REDE_KV}"
)

print(
    f"[MonitorDeRede] Banco: {HOSTS_TXT}"
)

print(
    f"[MonitorDeRede] Banco existe: "
    f"{Path(HOSTS_TXT).is_file()}"
)


# ============================================================
# CARREGAMENTO DO KV
# ============================================================

GUI = Builder.load_file(
    MONITOR_DE_REDE_KV
)


# ============================================================
# TELA DO MONITOR DE REDE
# ============================================================

class MonitorDeRede(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # ----------------------------------------------------
        # Lista que receberá as URLs vindas do SQLite.
        # ----------------------------------------------------

        self.urls = []


        # ----------------------------------------------------
        # Índice da próxima URL que será adicionada à interface.
        # ----------------------------------------------------

        self.indice_url = 0


        # ----------------------------------------------------
        # Quantidade de URLs adicionadas por lote.
        #
        # Como temos mais de 2.000 URLs, evitamos criar todos
        # os Labels de uma única vez.
        # ----------------------------------------------------

        self.tamanho_lote = 50


    # ========================================================
    # ENTRADA NA TELA
    # ========================================================

    def on_pre_enter(self, *args):
        """
        Executado antes da tela aparecer.

        Aqui iniciamos a leitura do banco em uma thread
        separada para não bloquear a interface do Kivy.
        """

        # ----------------------------------------------------
        # Reiniciamos o índice.
        # ----------------------------------------------------

        self.indice_url = 0


        # ----------------------------------------------------
        # Limpamos a lista anterior.
        # ----------------------------------------------------

        self.urls.clear()


        # ----------------------------------------------------
        # Limpamos os Widgets anteriores.
        # ----------------------------------------------------

        self.ids.box.clear_widgets()


        # ----------------------------------------------------
        # Criamos a thread responsável pela leitura do banco.
        # ----------------------------------------------------

        threading.Thread(
            target=self.ler_thread,
            daemon=True
        ).start()


    # ========================================================
    # CONEXÃO COM SQLITE
    # ========================================================

    def conectar(self):
        """
        Abre a conexão com o banco SQLite.
        """

        return sqlite3.connect(
            str(HOSTS_TXT)
        )


    # ========================================================
    # LEITURA DO BANCO
    # ========================================================

    def ler_thread(self):
        """
        Executada em uma thread separada.

        A consulta ao SQLite acontece aqui para evitar
        bloquear a thread principal do Kivy.
        """

        conn = None

        try:

            # ------------------------------------------------
            # Abre o banco.
            # ------------------------------------------------

            conn = self.conectar()


            # ------------------------------------------------
            # Cria o cursor.
            # ------------------------------------------------

            curr = conn.cursor()


            # ------------------------------------------------
            # Consulta as URLs.
            # ------------------------------------------------

            curr.execute(
                "SELECT URLS FROM Dominios"
            )


            # ------------------------------------------------
            # Recupera todas as linhas.
            # ------------------------------------------------

            linhas = curr.fetchall()


            # ------------------------------------------------
            # fetchall() retorna tuplas.
            #
            # Exemplo:
            #
            # [
            # ("www.exemplo.com",),
            # ("www.exemplo2.com",),
            # ]
            #
            # Pegamos somente o primeiro elemento.
            # ------------------------------------------------

            urls = [
                linha[0]
                for linha in linhas
            ]


            # ------------------------------------------------
            # Diagnóstico.
            # ------------------------------------------------

            print(
                f"[MonitorDeRede] "
                f"{len(urls)} URLs encontradas."
            )


            # ------------------------------------------------
            # A thread do banco não altera diretamente
            # os Widgets do Kivy.
            #
            # Enviamos os dados para a thread principal.
            # ------------------------------------------------

            Clock.schedule_once(
                lambda dt: self.receber_urls(urls),
                0
            )


        except Exception as e:

            # ------------------------------------------------
            # Exibe o erro original no terminal.
            # ------------------------------------------------

            print(
                "[MonitorDeRede] "
                "Erro ao ler banco:"
            )

            traceback.print_exc()


            # ------------------------------------------------
            # IMPORTANTE:
            #
            # Não usamos diretamente "e" dentro do lambda.
            #
            # O Python libera a variável da exceção depois
            # que o bloco except termina.
            #
            # Por isso guardamos a mensagem antes.
            # ------------------------------------------------

            mensagem_erro = str(e)


            # ------------------------------------------------
            # Enviamos a mensagem para a thread principal.
            # ------------------------------------------------

            Clock.schedule_once(
                lambda dt: self.mostrar_erro(
                    mensagem_erro
                ),
                0
            )


        finally:

            # ------------------------------------------------
            # Fecha o banco somente se ele foi aberto.
            # ------------------------------------------------

            if conn is not None:

                conn.close()


    # ========================================================
    # RECEBIMENTO DAS URLs
    # ========================================================

    def receber_urls(self, urls):
        """
        Executada pela thread principal do Kivy.

        Aqui podemos começar a modificar a interface.
        """

        # ----------------------------------------------------
        # Guardamos as URLs.
        # ----------------------------------------------------

        self.urls = urls


        # ----------------------------------------------------
        # Diagnóstico.
        # ----------------------------------------------------

        print(
            f"[MonitorDeRede] "
            f"Preparando {len(self.urls)} URLs."
        )


        # ----------------------------------------------------
        # Começamos pelo primeiro lote.
        # ----------------------------------------------------

        self.adicionar_lote()


    # ========================================================
    # ADICIONA UM LOTE DE URLs
    # ========================================================

    def adicionar_lote(self, *args):
        """
        Adiciona uma quantidade limitada de URLs por vez.
        """

        # ----------------------------------------------------
        # Recuperamos o BoxLayout do arquivo KV.
        # ----------------------------------------------------

        box = self.ids.box


        # ----------------------------------------------------
        # Calculamos o final do lote atual.
        #
        # Exemplo:
        #
        # indice_url = 0
        # tamanho_lote = 50
        #
        # fim = 50
        # ----------------------------------------------------

        fim = min(
            self.indice_url + self.tamanho_lote,
            len(self.urls)
        )


        # ----------------------------------------------------
        # Pegamos somente as URLs deste lote.
        # ----------------------------------------------------

        lote = self.urls[
            self.indice_url:fim
        ]


        # ----------------------------------------------------
        # Criamos um Label para cada URL.
        # ----------------------------------------------------

        for url in lote:

            label = Label(

                text=str(url),

                size_hint_y=None,

                height=45,

                halign="left",

                valign="middle",

                text_size=(None, 45),
            )


            # ------------------------------------------------
            # Adicionamos o Label ao BoxLayout.
            # ------------------------------------------------

            box.add_widget(label)


        # ----------------------------------------------------
        # Atualizamos o índice.
        # ----------------------------------------------------

        self.indice_url = fim


        # ----------------------------------------------------
        # Verificamos se ainda existem URLs.
        # ----------------------------------------------------

        if self.indice_url < len(self.urls):

            # ------------------------------------------------
            # Ainda existem URLs.
            #
            # Agendamos o próximo lote para o próximo ciclo
            # do Kivy.
            # ------------------------------------------------

            Clock.schedule_once(
                self.adicionar_lote,
                0
            )

        else:

            # ------------------------------------------------
            # Terminamos.
            # ------------------------------------------------

            print(
                "[MonitorDeRede] "
                "Todas as URLs foram adicionadas "
                "à interface."
            )


    # ========================================================
    # MENSAGEM DE ERRO
    # ========================================================

    def mostrar_erro(self, mensagem):
        """
        Recebe uma mensagem de erro enviada pela thread
        do banco.
        """

        print(
            f"[MonitorDeRede] {mensagem}"
        )


# ============================================================
# BOTÃO COM IMAGEM
# ============================================================

class ImageButton(ButtonBehavior, Image):
    pass


# ============================================================
# BOTÃO ARREDONDADO
# ============================================================

class RoundedButton(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        # ----------------------------------------------------
        # Fundo padrão transparente.
        # ----------------------------------------------------

        self.background_color = (
            0,
            0,
            0,
            0
        )


        # ----------------------------------------------------
        # Desenhamos nosso próprio fundo.
        # ----------------------------------------------------

        with self.canvas.before:

            Color(
                0,
                0,
                0,
                0.6
            )


            self.rect = RoundedRectangle(
                radius=[50],
                pos=self.pos,
                size=self.size
            )


            # ------------------------------------------------
            # Atualizamos o retângulo quando o botão mudar
            # de posição ou tamanho.
            # ------------------------------------------------

            self.bind(
                pos=self.update_rect,
                size=self.update_rect
            )


    def update_rect(self, *args):

        self.rect.pos = self.pos

        self.rect.size = self.size
