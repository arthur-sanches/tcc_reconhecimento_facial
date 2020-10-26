import sys
import time
import queue
import threading
from PyQt5.QtWidgets import QDialog, QApplication
from interface_operador import *
from server import executa_servidor


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def carregaLogs(self):
        try:
            with open("logs.txt", "r") as f:
                logs = ""
                lines = f.readlines()
                for line in reversed(lines):
                    logs += line
                self.ui.textBrowserLogs.setText(logs)
        except:
            with open("logs.txt", "w") as f:
                pass
        finally:
            pass

    def atualizaLogs(self, log):
        self.ui.textBrowserLogs.insertPlainText(log)


def inicia_servidor(interface):
    servidor_ligado = True
    fila_servidor = queue.Queue()
    t_servidor = threading.Thread(
        target=executa_servidor, args=(servidor_ligado, fila_servidor, interface))
    t_servidor.start()
    return fila_servidor, t_servidor


def encerra_servidor(fila_servidor, t_servidor):
    servidor_ligado = False
    fila_servidor.put(servidor_ligado)
    t_servidor.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = MyForm()
    interface.show()
    interface.carregaLogs()
    fila_servidor, t_servidor = inicia_servidor(interface)
    execution = app.exec_()
    encerra_servidor(fila_servidor, t_servidor)
    time.sleep(0.02)
    sys.exit(execution)
