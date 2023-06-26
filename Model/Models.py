import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
from View.main_form import Ui_MainForm
from View.form_operacao_manual import Ui_formManual
from Controller.Teclados import NumericKeyboard, AlphanumericKeyboard
import time

class Atualizador(QObject):
    sinal_atualizar = pyqtSignal(str, str)

    def __init__(self, operacao_manual):
        super().__init__()
        self.operacao_manual = operacao_manual
        self._running = True

    def atualizar_valor(self):
        while self._running == True:
            # Obtém o valor atualizado do dado (ou qualquer outra lógica necessária)
            valor_atualizado = str(self.operacao_manual.dado.temp.temperatura)
            valor_atualizado_fria = str( self.operacao_manual.dado.temp.temperatura_fria )
            # print(valor_atualizado)

            # Emite o sinal para atualizar a interface do usuário
            self.sinal_atualizar.emit(valor_atualizado, valor_atualizado_fria)

            # Aguarda 1 segundo antes de atualizar novamente
            QApplication.processEvents()
            time.sleep(1)

    def parar(self):
        self._running = False


class MainWindow(QMainWindow):
    def __init__(self, dado=None):
        super().__init__()

        self.janela_teste_saida = None
        self.dado = dado

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

        self.ui.btManual.clicked.connect(self.operacao_manual)

    def operacao_manual(self):
        self.janela_operacao_manual = OperacaoManual(dado=self.dado)
        #self.janela2.showMaximized()
        self.janela_operacao_manual.exec_()
        # self.hide()
        # self.close()

class OperacaoManual(QDialog):
    def __init__(self, dado=None):
        super().__init__()

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_formManual()
        self.ui.setupUi(self)
        self.dado = dado

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        self.ui.btVoltar.clicked.connect(self.voltar)
        self.ui.txSetPointQuente.mousePressEvent = self.teclado_set_point_quente
        self.ui.txSetPointFrio.mousePressEvent = self.teclado_set_point_frio
        self.ui.btLigaQuente.clicked.connect(self.liga_controle_resistencias)
        self.ui.btDesligaQuente.clicked.connect(self.desliga_controle_resistencias)
        self.ui.btLigaFrio.clicked.connect(self.liga_controle_refrigeracao)
        self.ui.btDesligaFrio.clicked.connect(self.desliga_controle_refrigeracao)

        self.ui.txSetPointQuente.setText(str(self.dado.temperatura_quente_set_point))
        self.ui.txSetPointFrio.setText(str(self.dado.temperatura_fria_set_point))

        # Inicializar o atualizador em uma nova thread
        self.atualizador = Atualizador(self)
        self.atualizador.sinal_atualizar.connect(self.atualizar_valor)
        self.atualizador_thread = QThread()
        self.atualizador.moveToThread(self.atualizador_thread)
        self.atualizador_thread.started.connect(self.atualizador.atualizar_valor)
        self.atualizador_thread.start()

    def teclado_set_point_quente(self, event):
        numeric_keyboard = NumericKeyboard(dado=self.dado, mode = 'quente')
        
        numeric_keyboard.exec_() # Roda como modal
        self.ui.txSetPointQuente.setText(str(self.dado.valor_teclado_setpoint_quente))
        self.dado.set_temperatura_quente_setpoint( float( self.ui.txSetPointQuente.text() ) )

    def teclado_set_point_frio(self, event):
        numeric_keyboard = NumericKeyboard(dado=self.dado, mode = 'frio')

        numeric_keyboard.exec_() # Roda como modal
        self.ui.txSetPointFrio.setText(str(self.dado.valor_teclado_setpoint_frio))
        self.dado.set_temperatura_fria_setpoint( float( self.ui.txSetPointFrio.text() ) )

    def voltar(self):
        self.close()# Chama o evento closedEvent

    def atualizar_valor(self, valor_quente, valor_frio):
        self.ui.txTemperaturaQuente.setText(valor_quente)
        self.ui.txTemperaturaFrio.setText(valor_frio)

    def liga_controle_resistencias(self):
        self.dado._controle_quente_estah_acionado = True

    def desliga_controle_resistencias(self):
        self.dado._controle_quente_estah_acionado = False

    def liga_controle_refrigeracao(self):
        self.dado._controle_frio_estah_acionado = True

    def desliga_controle_refrigeracao(self):
        self.dado._controle_frio_estah_acionado = False

    def closeEvent(self, event):
        # self.origem = MainWindow()
        # self.origem.showMaximized()
        # self.origem.show()
        # event.accept()# esse método aceita o pedido de fechamento....
        self.atualizador.parar()  # Parar a thread do atualizador
        self.atualizador_thread.quit()
        self.atualizador_thread.wait()
