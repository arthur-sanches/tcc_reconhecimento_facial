import sys
import time
import queue
import threading
import shutil
import os
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import QTextCursor

from interface_operador import *
from server import executa_servidor
from utils import nome_arquivo
from encode_faces import encode_faces


class MyForm(QDialog):
    def __init__(self, app):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.app = app
        self.__cursorLogs = QTextCursor(self.ui.textBrowserLogs.document())
        self.__carregaLogs()
        self.__imagens = []
        self.fila_servidor, self.fila_encoding, self.servidor = self.inicia_servidor()
        self.ui.pushButtonSelectImgs.clicked.connect(
            self.__selecionaImagens)
        self.ui.pushButtonCadastrar.clicked.connect(
            self.__cadastraUsuario)
        self.app.aboutToQuit.connect(self.encerra_servidor)
        self.show()

    def __carregaLogs(self):
        try:
            self.__cursorLogs.setPosition(0)
            self.ui.textBrowserLogs.setTextCursor(self.__cursorLogs)
            with open("logs.txt", "r") as f:
                lines = f.readlines()
            logs = ""
            for line in reversed(lines):
                logs += line
            self.ui.textBrowserLogs.setText(logs)
        except:
            with open("logs.txt", "x") as f:
                pass
        finally:
            pass

    def atualizaLogs(self, log):
        self.__cursorLogs.setPosition(0)
        self.ui.textBrowserLogs.setTextCursor(self.__cursorLogs)
        self.ui.textBrowserLogs.insertPlainText(log)

    def limpaLabelsCadastro(self):
        self.ui.labelImg1.clear()
        self.ui.labelImg2.clear()
        self.ui.labelImg3.clear()
        self.ui.labelImg4.clear()
        self.ui.labelImg5.clear()
        self.ui.labelAviso.clear()

    def __selecionaImagens(self):
        self.limpaLabelsCadastro()
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

        self.__imagens = fname[0]

    def __cadastraUsuario(self):
        self.limpaLabelsCadastro()
        if len(self.__imagens) <= 2:
            self.ui.labelAviso.setText("Número insuficiente de imagens!")
            return
        nome = self.ui.lineEditNome.text()
        rg = self.ui.lineEditRG.text()
        caminho_pasta = f"usuarios/{nome}-{rg}/"
        if os.path.exists(caminho_pasta):
            self.ui.labelAviso.setText("Esse usuário já está cadastrado.")
            return
        os.makedirs(caminho_pasta)
        for imagem in self.__imagens:
            shutil.copy(imagem, caminho_pasta)
        # gera encodings e envia para o raspberry
        encode_faces()
        self.fila_encoding.put(True)
        self.ui.labelImg3.setText("Usuário cadastrado com sucesso!")


    def inicia_servidor(self):
        servidor_ligado = True
        fila_encoding = queue.Queue()
        fila_encoding.put(True)
        fila_servidor = queue.Queue()
        t_servidor = threading.Thread(
            target=executa_servidor, args=(servidor_ligado, fila_servidor, fila_encoding, self))
        t_servidor.start()
        return fila_servidor, fila_encoding, t_servidor


    def encerra_servidor(self):
        self.fila_servidor.put(False)
        self.servidor.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = MyForm(app)
    execution = app.exec_()
    time.sleep(0.02)
    sys.exit(execution)
