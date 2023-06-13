import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from View.main_form import Ui_MainForm
from View.form_operacao_manual import Ui_formManual

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
        self.janela_operacao_manual.show()
        # self.hide()
        self.close()

class OperacaoManual(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_formManual()
        self.ui.setupUi(self)

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
        print(event)

    def voltar(self):
        self.close()# Chama o evento closedEvent

    def closeEvent(self, event):
        self.origem = MainWindow()
        #self.origem.showMaximized()
        self.origem.show()
        event.accept()# esse método aceita o pedido de fechamento....
