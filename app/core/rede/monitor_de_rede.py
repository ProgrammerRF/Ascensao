import subprocess
import threading
import sys
from pathlib import Path


class MonitorDeRede:

    def __init__(self):
        self.processo_wfplp = None
        self.thread_wfplp = None

    def monitoramento(self):
        """
        Inicia o monitoramento WFP em uma thread independente.
        """

        self.thread_wfplp = threading.Thread(
            target=self.wfplpblocker,
            name="WfplpBlocker",
            daemon=False
        )

        self.thread_wfplp.start()

    def _diretorio_recursos(self) -> Path:
        """
        Localiza os recursos tanto em desenvolvimento quanto
        no executável gerado pelo PyInstaller.
        """

        if getattr(sys, "frozen", False):
            return Path(sys._MEIPASS)

        return Path(__file__).resolve().parent.parent.parent.parent

    def wfplpblocker(self):

        try:

            diretorio = self._diretorio_recursos()

            executavel = (
                diretorio
                / "bin"
                / "WfplpBlocker.exe"
            )

            banco = Path(
                r"C:\Ascensao\app\database\dominios.db"
            )

            # -------------------------------------------------
            # Validações
            # -------------------------------------------------

            if not executavel.is_file():

                print(
                    "[WfplpBlocker] ERRO: "
                    f"executável não encontrado: {executavel}"
                )

                return

            if not banco.is_file():

                print(
                    "[WfplpBlocker] ERRO: "
                    f"banco não encontrado: {banco}"
                )

                return

            # -------------------------------------------------
            # Comando
            # -------------------------------------------------

            comando = [
                str(executavel),
                str(banco),
            ]

            print(
                "[WfplpBlocker] Executando:"
                f"\n {executavel}"
                f"\n {banco}"
            )

            # -------------------------------------------------
            # Inicia o processo C
            # -------------------------------------------------

            self.processo_wfplp = subprocess.Popen(

                comando,

                stdin=subprocess.PIPE,

                stdout=subprocess.PIPE,

                stderr=subprocess.STDOUT,

                text=True,

                encoding="utf-8",

                errors="replace",

                bufsize=1,

                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            # -------------------------------------------------
            # Lê a saída do C
            # -------------------------------------------------

            if self.processo_wfplp.stdout is not None:

                for linha in self.processo_wfplp.stdout:

                    print(
                        "[WfplpBlocker] "
                        f"{linha.rstrip()}"
                    )

            # -------------------------------------------------
            # Aguarda o processo terminar
            # -------------------------------------------------

            codigo = self.processo_wfplp.wait()

            print(
                "[WfplpBlocker] "
                f"encerrado. Código: {codigo}"
            )

        except FileNotFoundError as erro:

            print(
                "[WfplpBlocker] "
                f"Arquivo não encontrado: {erro}"
            )

        except Exception as erro:

            print(
                "[WfplpBlocker] "
                f"Erro inesperado: {erro}"
            )

    def parar(self):
        """
        Solicita o encerramento gracioso do WfplpBlocker.
        """

        processo = self.processo_wfplp

        # -----------------------------------------------------
        # Não existe processo
        # -----------------------------------------------------

        if processo is None:

            print(
                "[WfplpBlocker] "
                "Nenhum processo para encerrar."
            )

            return

        # -----------------------------------------------------
        # Processo já terminou
        # -----------------------------------------------------

        if processo.poll() is not None:

            print(
                "[WfplpBlocker] "
                "Processo já estava encerrado."
            )

            return

        # -----------------------------------------------------
        # Envia STOP para o C
        # -----------------------------------------------------

        try:

            if processo.stdin is not None:

                print(
                    "[WfplpBlocker] "
                    "Enviando STOP..."
                )

                processo.stdin.write("STOP\n")

                processo.stdin.flush()

                processo.stdin.close()

        except (BrokenPipeError, OSError) as erro:

            print(
                "[WfplpBlocker] "
                f"Erro ao enviar STOP: {erro}"
            )

        # -----------------------------------------------------
        # Aguarda o C terminar
        # -----------------------------------------------------

        try:

            codigo = processo.wait(timeout=10)

            print(
                "[WfplpBlocker] "
                "encerramento concluído. "
                f"Código: {codigo}"
            )

        except subprocess.TimeoutExpired:

            print(
                "[WfplpBlocker] "
                "O processo não encerrou após STOP."
            )

            # -------------------------------------------------
            # Último recurso
            # -------------------------------------------------

            try:

                processo.terminate()

                processo.wait(timeout=3)

                print(
                    "[WfplpBlocker] "
                    "Processo terminado à força."
                )

            except subprocess.TimeoutExpired:

                print(
                    "[WfplpBlocker] "
                    "terminate() não foi suficiente. "
                    "Executando kill()."
                )

                processo.kill()

                processo.wait()

        finally:

            self.processo_wfplp = None


monitor = MonitorDeRede()
