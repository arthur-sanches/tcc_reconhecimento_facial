import sys
import time
import queue
import threading
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from interface_operador import *
from server import executa_servidor
from utils import nome_arquivo


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.__carregaLogs()
        imagens = self.ui.pushButtonSelectImgs.clicked.connect(
            self.selecionaImagens)

    def __carregaLogs(self):
        try:
            with open("logs.txt", "r") as f:
                logs = ""
                lines = f.readlines()
                for line in reversed(lines):
                    logs += line
                self.ui.textBrowserLogs.setText(logs)
        except:
            with open("logs.txt", "x") as f:
                pass
        finally:
            pass

    def atualizaLogs(self, log):
        self.ui.textBrowserLogs.insertPlainText(log)

    def selecionaImagens(self):
        self.ui.labelImg1.clear()
        self.ui.labelImg2.clear()
        self.ui.labelImg3.clear()
        self.ui.labelImg4.clear()
        self.ui.labelImg5.clear()
        self.ui.labelAviso.clear()

        fname = QFileDialog.getOpenFileNames(
            self, 'Open file', '/home', "Image files (*.jpg *.jpeg *.png)")

        if len(fname[0]) >= 1:
            self.ui.labelImg1.setText(nome_arquivo(fname[0][0]))
        if len(fname[0]) >= 2:
            self.ui.labelImg2.setText(nome_arquivo(fname[0][1]))
        if len(fname[0]) >= 3:
            self.ui.labelImg3.setText(nome_arquivo(fname[0][2]))
        else:
            self.ui.labelAviso.setText("Escolha pelo menos 3 imagens!")
        if len(fname[0]) >= 4:
            self.ui.labelImg4.setText(nome_arquivo(fname[0][3]))
        if len(fname[0]) >= 5:
            self.ui.labelImg5.setText(nome_arquivo(fname[0][4]))

        return fname[0]

    def cadastraUsuario(self, imagens):
        for imagem in imagens:
            pass


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
    fila_servidor, t_servidor = inicia_servidor(interface)
    execution = app.exec_()
    encerra_servidor(fila_servidor, t_servidor)
    time.sleep(0.02)
    sys.exit(execution)
