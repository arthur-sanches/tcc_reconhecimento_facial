import sys
from PyQt5.QtWidgets import QDialog, QApplication
from interface_operador import *

class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.carregaLogs()
        #self.ui.buttonClickMe.clicked.connect(self.dispmessage)
        #self.show()
    #def dispmessage(self):
        #self.ui.label.setText("Hello " + self.ui.lineEditName.text())

    def carregaLogs(self):
        with open("logs.txt", "r") as f:
            self.ui.textBrowserLogs.setText(f.read())

    def atualizaLogs(self, log):
        self.ui.textBrowserLogs.append(log)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = MyForm()
    interface.show()
    sys.exit(app.exec_())
