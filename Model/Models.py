import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt
from View.main_form import Ui_MainForm
from View.form_operacao_manual import Ui_formManual
from Controller.Teclados import NumericKeyboard, AlphanumericKeyboard
from Controller.Dados import Dado

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.janela_teste_saida = None

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        self.ui.btManual.clicked.connect(self.voltar)

    def voltar(self):
        self.janela_operacao_manual = OperacaoManual()
        #self.janela2.showMaximized()
        self.janela_operacao_manual.exec_()
        # self.hide()
        # self.close()

class OperacaoManual(QDialog):
    def __init__(self):
        super().__init__()

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_formManual()
        self.ui.setupUi(self)
        self.dado = Dado()

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        self.ui.btVoltar.clicked.connect(self.voltar)
        self.ui.txTemperatura.mousePressEvent = self.teclado

    def teclado(self, event):
        numeric_keyboard = NumericKeyboard(dado=self.dado)
        
        numeric_keyboard.exec_() # Roda como modal
        self.ui.txTemperatura.setText(self.dado.valor_teclado)

    # def show(self):
    #     print("Está visivel")

    def voltar(self):
        self.close()# Chama o evento closedEvent

    def closeEvent(self, event):
        # self.origem = MainWindow()
        #self.origem.showMaximized()
        # self.origem.show()
        # event.accept()# esse método aceita o pedido de fechamento....
        pass
