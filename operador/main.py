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
        self.carregaLogs()

    def carregaLogs(self):
        with open("logs.txt", "r") as f:
            self.ui.textBrowserLogs.setText(f.read())

    def atualizaLogs(self, log):
        self.ui.textBrowserLogs.append(log)


def inicia_servidor():
    servidor_ligado = True
    fila_servidor = queue.Queue()
    t_servidor = threading.Thread(
        target=executa_servidor, args=(servidor_ligado, fila_servidor))
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
    fila_servidor, t_servidor = inicia_servidor()
    execution = app.exec_()
    encerra_servidor(fila_servidor, t_servidor)
    time.sleep(0.02)
    sys.exit(execution)
