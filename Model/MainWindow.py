import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from View.main_form import Ui_MainForm

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