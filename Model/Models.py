import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox,QHeaderView, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QEventLoop
from PyQt5.QtCore import pyqtSlot
from View.main_form import Ui_MainForm
from View.form_operacao_manual import Ui_formManual
from View.form_config import Ui_FormConfig
from View.form_view_programas import Ui_FormViewProgramas
from View.form_iniciar import Ui_FormIniciar
from Controller.Teclados import NumericKeyboard, AlphanumericKeyboard
import time

from Xlib import X, display

from Controller.Dados import Dado
from Controller.ControleProporcional import ControleProporcional, ControleFrio
from Controller.Ios import InOut
from Controller.DataBase import DataBase
from Controller.SimpleMessage import SimpleMessageBox


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
    def __init__(self, dado=None, io=None):
        super().__init__()

        self.janela_teste_saida = None
        self.dado = dado
        self.io = io

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        # screen = QApplication.primaryScreen()
        # mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        # self.move(mainScreenRect.topLeft())
        self.move(0,0)
    
        self.ui.btManual.clicked.connect(self.operacao_manual)
        self.ui.btConfig.clicked.connect(self.configuracao)
        self.ui.btIniciar.clicked.connect(self.iniciar)
        self.mouseReleaseEvent = self.setfoccus
        self.ui.txHidden.keyReleaseEvent = self.eventoteclado

        # faz com que o objeto fique invisível
        self.ui.txHidden.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: none;")

    def operacao_manual(self):
        self.janela_operacao_manual = OperacaoManual(dado=self.dado, io=self.io)
        #self.janela2.showMaximized()
        self.janela_operacao_manual.exec_()
        # self.hide()
        # self.close()

    def configuracao(self):
        configuracao = Configuracao(dado=self.dado, io=self.io)
        configuracao.exec_()

    def iniciar(self):
        view = ViewProgamas()

        view.exec_()
        db_loc = DataBase()
        prog_loc = db_loc.search_record_by_name(view.nome_programa)

        try:

            self.dado.set_nome_programa_ciclo(prog_loc[1])
            self.dado.set_setpoint_quente_ciclo(prog_loc[2])
            self.dado.set_setpoint_frio_ciclo(prog_loc[3])
            self.dado.set_tempo_parte_quente_ciclo(prog_loc[4])
            self.dado.set_tempo_parte_fria_ciclo(prog_loc[5])
            self.dado.set_quantidade_de_ciclo(prog_loc[6])
            self.dado.set_potencia_ventilador_ciclo(prog_loc[7])
            self.dado.set_controle_proporcional_ciclo(prog_loc[8])
            self.dado.set_inicio_do_ciclo(prog_loc[9])
            self.dado.set_estabilizar_temperatura_ciclo(prog_loc[10])

            iniciar = IniciarCiclagem(dado=self.dado, io=self.io)
            iniciar.exec_()

        except TypeError as e:
            print(f"Erro no carregamento de proc_loc:\n{e}")

    def showEvent(self, event):
        # Sobrescrevendo o evento 'showEvent' para ajustar a posição após a janela ser exibida
        # screen = QApplication.desktop().screenGeometry(self)
        # taskbar_height = QApplication.desktop().height() - screen.height()

        # Define a posição vertical da janela para que ela fique alinhada à barra de ferramentas do sistema
        # self.move(self.x(), QApplication.desktop().height() - self.height() - taskbar_height)

        super().showEvent(event)

    def closeEvent(self, event):
        event.accept()

    def setfoccus(self, event):
        self.ui.txHidden.clear()
        self.ui.txHidden.setFocus()

    def eventoteclado(self, event):
        carac = event.text()
        if carac == 'q' or carac == 'Q':
            self.close()

class OperacaoManual(QDialog):
    def __init__(self, dado=None, io = None):
        super().__init__()

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_formManual()
        self.ui.setupUi(self)
        self.dado = dado
        self.io = io

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        self.ui.btVoltar.clicked.connect(self.voltar)
        self.ui.txSetPointQuente.mousePressEvent = self.teclado_set_point_quente
        self.ui.txSetPointFrio.mousePressEvent = self.teclado_set_point_frio
        self.ui.txVeloVentilacao.mousePressEvent = self.teclado_set_velo_ventilacao

        self.ui.btLigaQuente.clicked.connect(self.liga_controle_resistencias)
        self.ui.btDesligaQuente.clicked.connect(self.desliga_controle_resistencias)

        self.ui.btLigaFrio.clicked.connect(self.liga_controle_refrigeracao)
        self.ui.btDesligaFrio.clicked.connect(self.desliga_controle_refrigeracao)

        self.ui.btElevadorSobe.clicked.connect(self.sobe_elevador)
        self.ui.btElevadorDesce.clicked.connect(self.desce_elevador)

        self.ui.txSetPointQuente.setText(str(self.dado.temperatura_quente_set_point))
        self.ui.txSetPointFrio.setText(str(self.dado.temperatura_fria_set_point))
        self.ui.txVeloVentilacao.setText(str(self.dado.pwm_circulacao_fria))

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
        self.ui.txSetPointQuente.setText(str(self.dado.temperatura_quente_set_point))
        self.dado.set_temperatura_quente_setpoint( float( self.ui.txSetPointQuente.text() ) )

    def teclado_set_point_frio(self, event):
        numeric_keyboard = NumericKeyboard(dado=self.dado, mode = 'frio')

        numeric_keyboard.exec_() # Roda como modal
        self.ui.txSetPointFrio.setText(str(self.dado.temperatura_fria_set_point))
        self.dado.set_temperatura_fria_setpoint( float( self.ui.txSetPointFrio.text() ) )

    def teclado_set_velo_ventilacao(self, event):
        numeric_keyboard = NumericKeyboard(dado=self.dado, mode='velo_circulacao')

        numeric_keyboard.exec_()
        self.ui.txVeloVentilacao.setText(str(self.dado.pwm_circulacao_fria))
        self.dado.set_pwm_circulacao_fria( float(self.ui.txVeloVentilacao.text()) )

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

    def sobe_elevador(self):
        self.io.elevador(1)

    def desce_elevador(self):
        self.io.elevador(0)

    def closeEvent(self, event):
        # self.origem = MainWindow()
        # self.origem.showMaximized()
        # self.origem.show()
        # event.accept()# esse método aceita o pedido de fechamento....
        self.atualizador.parar()  # Parar a thread do atualizador
        self.atualizador_thread.quit()
        self.atualizador_thread.wait()

class IniciarCiclagem(QDialog):
    def __init__(self, dado=None, io = None):
        super().__init__()

        self.ui = Ui_FormIniciar()
        self.ui.setupUi(self)
        self.dado = dado
        self.io = io

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        # Variáveis controle de ciclo e tempo
        self.tempo_corrente_quente = 1
        self.tempo_corrente_frio = 1
        self.qtd_ciclo_corrente = 1
        self.estado_ciclagem = 'inicio'
        self.fim_de_ciclo = False

        self.BASE_TEMPO = 60

        self.toggle_img = True
        self.controle_local = False
        self.font = QtGui.QFont()

        # Preenche os valores dos campos de label
        self.setTextLabel(str(self.dado.nome_programa_ciclo), self.ui.lbNomeProgCiclo, align='center')
        self.setTextLabel(str( self.dado.setpoint_quente_ciclo ), self.ui.lbSetpointQuente)
        self.setTextLabel(str(self.dado.setpoint_frio_ciclo), self.ui.lbSetpointFrio)

        self.ui.btCancelar.clicked.connect(self.cancelar)
        self.ui.btIniciarPausar.clicked.connect(self.aciona_controle)

        if self.dado.inicio_do_ciclo == 'quente':
            self.io.elevador(1)
        elif self.dado.inicio_do_ciclo == 'frio':
            self.io.elevador(0)

        # Inicializar o atualizador em uma nova thread
        self.atualizador = Atualizador(self)
        self.atualizador.sinal_atualizar.connect(self.atualizar_valor)
        self.atualizador_thread = QThread()
        self.atualizador.moveToThread(self.atualizador_thread)
        self.atualizador_thread.started.connect(self.atualizador.atualizar_valor)
        self.atualizador_thread.start()

    def atualizar_valor(self, valor_quente, valor_frio):
        self.setTextLabel(valor_quente, self.ui.lbTemperaturaQuente)
        self.setTextLabel(valor_frio, self.ui.lbTemperaturaFria)

        self.setTextLabel(str(f"{int(self.tempo_corrente_quente/self.BASE_TEMPO+1)} de {self.dado.tempo_parte_quente_ciclo}"), self.ui.lbTempoQuente)
        self.setTextLabel(str(f"{int(self.tempo_corrente_frio/self.BASE_TEMPO+1)} de {self.dado.tempo_parte_fria_ciclo}"), self.ui.lbTempoFrio)
        self.setTextLabel(str(f"{self.qtd_ciclo_corrente} de {self.dado.quantidade_de_cliclo}"), self.ui.lbQtdCiclo)

        if self.io.status_elevador == "quente":
            self.ui.lbElevador.setGeometry(QtCore.QRect(290, 120, 81, 71))
            if self.toggle_img == True  and self.controle_local == True:
                self.ui.lbElevador.setStyleSheet("background-color: rgb(172, 0, 4);")
            else:
                self.ui.lbElevador.setStyleSheet("background-color: rgb(174, 174, 174);")
            self.toggle_img = not self.toggle_img
        elif self.io.status_elevador == "frio":
            self.ui.lbElevador.setGeometry(QtCore.QRect(290,250,81,71))

            if self.toggle_img == False and self.controle_local == True:
                self.ui.lbElevador.setStyleSheet("background-color: rgb(0, 189, 173);")
            else:
                self.ui.lbElevador.setStyleSheet("background-color: rgb(174, 174, 174);")
            self.toggle_img = not self.toggle_img

        if self.controle_local == True:
            if self.estado_ciclagem == "inicio":
                if (float(valor_quente) >= self.dado.setpoint_quente_ciclo) and (float(valor_frio) <= self.dado.setpoint_frio_ciclo):
                    self.estado_ciclagem = "meio"
            elif self.estado_ciclagem == "meio" and self.dado.estabilizar_temperatura_ciclo == "sim":
                if (float(valor_quente) >= self.dado.setpoint_quente_ciclo*0.98) and (float(valor_frio) <= self.dado.setpoint_frio_ciclo*1.02):
                    if self.io.status_elevador == "quente":
                        self.tempo_corrente_quente += 1
                        if self.tempo_corrente_quente > int(self.dado.tempo_parte_quente_ciclo)*self.BASE_TEMPO:
                            self.tempo_corrente_quente = 1
                            self.io.elevador(self.io.PARTE_FRIA)
                            if self.dado.inicio_do_ciclo == "frio":
                                self.qtd_ciclo_corrente += 1
                    if self.io.status_elevador == "frio":
                        self.tempo_corrente_frio +=1
                        if self.tempo_corrente_frio > int(self.dado.tempo_parte_fria_ciclo)*self.BASE_TEMPO:
                            self.tempo_corrente_frio = 1
                            self.io.elevador(self.io.PARTE_QUENTE)
                            if self.dado.inicio_do_ciclo == "quente":
                                self.qtd_ciclo_corrente += 1
                    if self.qtd_ciclo_corrente > self.dado.quantidade_de_cliclo:
                        self.controle_local = False
                        self.qtd_ciclo_corrente = 1
                        self.tempo_corrente_quente = 1
                        self.tempo_corrente_frio = 1
                        self.estado_ciclagem = "inicio"
                        self.dado._controle_quente_estah_acionado = False
                        self.dado._controle_frio_estah_acionado = False
                        self.fim_de_ciclo = True

            elif self.estado_ciclagem == "meio" and self.dado.estabilizar_temperatura_ciclo == "nao":
                if self.io.status_elevador == "quente":
                    self.tempo_corrente_quente += 1
                    if self.tempo_corrente_quente > int(self.dado.tempo_parte_quente_ciclo)*self.BASE_TEMPO:
                        self.tempo_corrente_quente = 1
                        self.io.elevador(self.io.PARTE_FRIA)
                        if self.dado.inicio_do_ciclo == "frio":
                            self.qtd_ciclo_corrente += 1
                if self.io.status_elevador == "frio":
                    self.tempo_corrente_frio +=1
                    if self.tempo_corrente_frio > int(self.dado.tempo_parte_fria_ciclo)*self.BASE_TEMPO:
                        self.tempo_corrente_frio = 1
                        self.io.elevador(self.io.PARTE_QUENTE)
                        if self.dado.inicio_do_ciclo == "quente":
                            self.qtd_ciclo_corrente += 1
                if self.qtd_ciclo_corrente > self.dado.quantidade_de_cliclo:
                    self.controle_local = False
                    self.qtd_ciclo_corrente = 1
                    self.tempo_corrente_quente = 1
                    self.tempo_corrente_frio = 1
                    self.estado_ciclagem = "inicio"
                    self.dado._controle_quente_estah_acionado = False
                    self.dado._controle_frio_estah_acionado = False
                    self.fim_de_ciclo = True

        else:
            if self.fim_de_ciclo == True:
                if self.toggle_img == False:
                    self.setTextLabel(f"{self.dado.nome_programa_ciclo} Finalizou", self.ui.lbNomeProgCiclo, align="center")
                else:
                    self.setTextLabel(f"##########################", self.ui.lbNomeProgCiclo, align="center")
                self.toggle_img = not self.toggle_img

    def setTextLabel(self, texto, lb, align = 'left'):
        _translate = QtCore.QCoreApplication.translate

        if align == 'center':
            lb.setText(_translate("FormIniciar", f"<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\">{texto}</span></p></body></html>"))
        elif align == 'left':
            lb.setText(_translate("FormIniciar", f"<html><head/><body><p><span style=\" font-size:36pt;\">{texto}</span></p></body></html>"))

    def aciona_controle(self):
        if self.fim_de_ciclo == False:
            if self.dado._controle_quente_estah_acionado != self.dado._controle_frio_estah_acionado:
                self.dado._controle_quente_estah_acionado = False
                self.dado._controle_frio_estah_acionado = False

            self.dado._controle_quente_estah_acionado = not self.dado._controle_quente_estah_acionado
            self.dado._controle_frio_estah_acionado = not self.dado._controle_frio_estah_acionado

            self.font.setPointSize(28)
            self.font.setBold(True)
            self.font.setItalic(True)
            if self.dado._controle_quente_estah_acionado and self.dado._controle_quente_estah_acionado:
                self.controle_local = True
                
                self.ui.btIniciarPausar.setFont(self.font)
                self.ui.btIniciarPausar.setText("Pausar")
                self.dado._temperatura_quente_set_point = self.dado.setpoint_quente_ciclo
                self.dado._temperatura_fria_set_point = self.dado.setpoint_frio_ciclo
                self.dado._pwm_circulacao_fria = self.dado.potencia_ventilador_ciclo
                self.dado.set_ganho_proporcional(self.dado.controle_proporcional_ciclo)
            else:
                self.controle_local = False
                
                self.ui.btIniciarPausar.setFont(self.font)
                self.ui.btIniciarPausar.setText("Iniciar")

        

    def cancelar(self):
        self.fim_de_ciclo = False
        self.dado._controle_quente_estah_acionado = False
        self.dado._controle_frio_estah_acionado = False
        self.close()

    def closeEvent(self, event):
        self.atualizador.parar()  # Parar a thread do atualizador



class Configuracao(QDialog):
    def __init__(self, dado=None, io = None):
        super().__init__()

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_FormConfig()
        self.ui.setupUi(self)
        self.dado = dado
        self.io = io

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        self.ui.btCancelar.clicked.connect(self.cancelar)
        self.ui.btCriar.clicked.connect(self.criar)
        self.ui.btLocalizar.clicked.connect(self.procurar)
        self.ui.btDeletar.clicked.connect(self.deletar)
        self.ui.btAtualizar.clicked.connect(self.atualizar)

        self.ui.txNomePrograma.mousePressEvent = self.nome_programa
        self.ui.txSetPointQuente.mousePressEvent = self.setpoint_quente
        self.ui.txSetPointFrio.mousePressEvent = self.setpoint_frio
        self.ui.txTempoCamaraQuente.mousePressEvent = self.tempo_quente
        self.ui.txTempoCamaraFria.mousePressEvent = self.tempo_frio
        self.ui.txQuantidadeCiclos.mousePressEvent = self.qtd_ciclos
        self.ui.txPotenciaVentiladorFrio.mousePressEvent = self.potencia_ventilador
        self.ui.txControleProporcional.mousePressEvent = self.controle_proporcional

        self.database = DataBase()

        self.lista_programa = []

    def nome_programa(self, event):
        keyboard = AlphanumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txNomePrograma.setText(keyboard.line_edit.text())

    def setpoint_quente(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txSetPointQuente.setText(keyboard.line_edit.text())

    def setpoint_frio(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txSetPointFrio.setText(keyboard.line_edit.text())

    def tempo_quente(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txTempoCamaraQuente.setText(keyboard.line_edit.text())

    def tempo_frio(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txTempoCamaraFria.setText(keyboard.line_edit.text())

    def qtd_ciclos(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txQuantidadeCiclos.setText(keyboard.line_edit.text())

    def potencia_ventilador(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txPotenciaVentiladorFrio.setText(keyboard.line_edit.text())

    def controle_proporcional(self, event):
        keyboard = NumericKeyboard(dado=self.dado)
        keyboard.exec_() # Roda como modal
        self.ui.txControleProporcional.setText(keyboard.line_edit.text())

    def criar(self):

        dados_local = self.database.get_all_records()
        nome_buscar = self.ui.txNomePrograma.text()

        nome_programa_existe = any(registro[1] == nome_buscar for registro in dados_local)

        if nome_programa_existe:
            ms = SimpleMessageBox(message='Esse programa já existe!')
            ms.exec()
        else:
            lista_salvar, status_ = self.verificar_campos()

            if status_:
                self.database.create_record(lista_salvar)
                ms = SimpleMessageBox(message=f'O Programa {self.ui.txNomePrograma.text()} foi salvo com sucesso!')
                ms.exec()
                self.limpar_campos()
            else:
                ms = SimpleMessageBox(message='Favor verificar se os campos estão corretos')
                ms.exec()

    def popular_lista_campos(self):
        nome = self.ui.txNomePrograma.text()
        if nome != "":

            self.lista_programa.append(self.ui.txNomePrograma.text())
            self.lista_programa.append(float(self.ui.txSetPointQuente.text()))
            self.lista_programa.append(float(self.ui.txSetPointFrio.text()))
            self.lista_programa.append(int(self.ui.txTempoCamaraQuente.text()))
            self.lista_programa.append(int(self.ui.txTempoCamaraFria.text()))

            self.lista_programa.append(int(self.ui.txQuantidadeCiclos.text()))
            self.lista_programa.append(int(self.ui.txPotenciaVentiladorFrio.text()))
            self.lista_programa.append(float(self.ui.txControleProporcional.text()))

            inicio_ciclo = ""
            estabilizar = ""

            if self.ui.rbInicioCicloQuente.isChecked() == True:
                inicio_ciclo = "quente"
            elif self.ui.rbInicioCicloFrio.isChecked() == True:
                inicio_ciclo = "frio"

            if self.ui.rbAguardarTemperaturaSim.isChecked() == True:
                estabilizar = "sim"
            elif self.ui.rbAguardarTemperaturaNao.isChecked() == True:
                estabilizar = "nao"

            self.lista_programa.append(inicio_ciclo)
            self.lista_programa.append(estabilizar)

    def limpar_campos(self):
        self.ui.txNomePrograma.clear()
        self.ui.txSetPointQuente.clear()
        self.ui.txSetPointFrio.clear()
        self.ui.txTempoCamaraQuente.clear()
        self.ui.txTempoCamaraFria.clear()
        self.ui.txQuantidadeCiclos.clear()
        self.ui.txPotenciaVentiladorFrio.clear()
        self.ui.txControleProporcional.clear()



    def verificar_campos(self):
        try:
            inicio_ciclo = ''
            estabilizar = ''
            lista_salvar = []
            status = False
            if self.ui.rbInicioCicloQuente.isChecked() == True:
                inicio_ciclo = 'quente'
            elif self.ui.rbInicioCicloFrio.isChecked() == True:
                inicio_ciclo = 'frio'
            else:
                inicio_ciclo = 'quente'

            if self.ui.rbAguardarTemperaturaSim.isChecked() == True:
                estabilizar = 'sim'
            elif self.ui.rbAguardarTemperaturaNao.isChecked() == True:
                estabilizar = 'nao'
            else:
                estabilizar = 'nao'
            lista_salvar = [
                    self.ui.txNomePrograma.text(),
                    float(self.ui.txSetPointQuente.text()),
                    float(self.ui.txSetPointFrio.text()),
                    int(self.ui.txTempoCamaraQuente.text()),
                    int(self.ui.txTempoCamaraFria.text()),
                    int(self.ui.txQuantidadeCiclos.text()),
                    int(self.ui.txPotenciaVentiladorFrio.text()),
                    float(self.ui.txControleProporcional.text()),
                    inicio_ciclo,
                    estabilizar          
                ]
            status = True
        except:
            status = False
        return lista_salvar, status
    
    def procurar(self):
        view = ViewProgamas()

        view.exec_()
        db_loc = DataBase()
        prog_loc = db_loc.search_record_by_name(view.nome_programa)
        
        if prog_loc != None:
            self.ui.txNomePrograma.setText(prog_loc[1])
            self.ui.txSetPointQuente.setText(str(prog_loc[2]))
            self.ui.txSetPointFrio.setText(str(prog_loc[3]))

            self.ui.txTempoCamaraQuente.setText(str(prog_loc[4]))
            self.ui.txTempoCamaraFria.setText(str(prog_loc[5]))
            self.ui.txQuantidadeCiclos.setText(str(prog_loc[6]))
            self.ui.txPotenciaVentiladorFrio.setText(str(prog_loc[7]))
            self.ui.txControleProporcional.setText(str(prog_loc[8]))

            if prog_loc[9] == 'quente':
                self.ui.rbInicioCicloQuente.setChecked(True)
                self.ui.rbInicioCicloFrio.setChecked(False)
            elif prog_loc[9] == 'frio':
                self.ui.rbInicioCicloQuente.setChecked(False)
                self.ui.rbInicioCicloFrio.setChecked(True)

            if prog_loc[10] == 'sim':
                self.ui.rbAguardarTemperaturaSim.setChecked(True)
                self.ui.rbAguardarTemperaturaNao.setChecked(False)
            elif prog_loc[10] == 'nao':
                self.ui.rbAguardarTemperaturaSim.setChecked(False)
                self.ui.rbAguardarTemperaturaNao.setChecked(True)

    def deletar(self):
        nome = self.ui.txNomePrograma.text()
        if nome != '':
            db_loc = DataBase()
            prog_loc = db_loc.search_record_by_name(nome)
            if prog_loc != None:
                db_loc.delete_record(prog_loc[0])
                msg = SimpleMessageBox(message=f"O Programa: {nome} foi deletado com sucesso!!")
                msg.exec()
                self.limpar_campos()
    
    def atualizar(self):
        nome = self.ui.txNomePrograma.text()
        if nome != '':
            db_loc = DataBase()
            prog_loc = db_loc.search_record_by_name(nome)
            if prog_loc != None:
                self.popular_lista_campos()
                db_loc.update_record(record_id=prog_loc[0], data= list(self.lista_programa))
                self.lista_programa.clear()
                msg = SimpleMessageBox(message=f"O Programa: {nome} foi atualizado com sucesso!!")
                msg.exec()
                self.limpar_campos()


    def cancelar(self):
        self.close()
        

    def closeEvent(self, event):
        # Sobrescrevendo o evento 'closeEvent' para exibir a caixa de diálogo de confirmação ao fechar a janela
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Confirmação')
        msg_box.setText('Você deseja fechar a janela?')
        msg_box.setIcon(QMessageBox.Question)
        msg_box.addButton('Sim', QMessageBox.YesRole)
        msg_box.addButton('Não', QMessageBox.NoRole)

        # Personalizar o tamanho do layout do QMessageBox
        layout = msg_box.layout()
        msg_box.setLayout(layout)

        # Ajustar o tamanho da janela para se adequar ao layout personalizado
        msg_box.resize(900, 600)

        # Executar a caixa de diálogo e verificar o resultado
        loop = QEventLoop()
        msg_box.finished.connect(loop.quit)
        msg_box.open()
        loop.exec_()

        clicked_button = msg_box.clickedButton()
        if clicked_button is not None and msg_box.buttonRole(clicked_button) == QMessageBox.YesRole:
            event.accept()  # Aceita o evento de fechamento
        else:
            event.ignore()  # Ignora o evento de fechamento

class ViewProgamas(QDialog):
    def __init__(self, dado=None, io=None):
        super().__init__()

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_FormViewProgramas()
        self.ui.setupUi(self)
        self.dado = dado
        self.io = io
        self.nome_programa = ''

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Obter o tamanho do monitor primário
        screen = QApplication.primaryScreen()
        mainScreenRect = screen.availableGeometry()

        # Definir a posição da janela no canto superior esquerdo
        self.move(mainScreenRect.topLeft())

        # Crie o modelo de dados para a QTableView
        self.model = QStandardItemModel(self)

        # Defina os cabeçalhos da tabela
        self.model.setHorizontalHeaderLabels(['Nome do Programa', 'Setpoint Quente', 'Setpoint Fria'])

        # Crie uma conexão com o banco de dados
        self.database = DataBase()

        # Obtenha todos os registros do banco de dados
        records = self.database.get_all_records()

        # Preencha o QStandardItemModel com os registros
        for row_data in records:
            row_items = [QStandardItem(str(item)) for item in row_data[1:4]]  # Ignora a coluna "id"
            self.model.appendRow(row_items)

        # Conecte o QStandardItemModel à QTableView
        self.ui.tblViewProgramas.setModel(self.model)

        # Defina as colunas para que preencham toda a largura da tabela
        header = self.ui.tblViewProgramas.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Crie o layout para a janela
        layout = QVBoxLayout()
        layout.addWidget(self.ui.tblViewProgramas)
        self.setLayout(layout)

        # Conecte o sinal clicked da QTableView à função on_table_view_clicked
        self.ui.tblViewProgramas.clicked.connect(self.on_table_view_clicked)

        self.ui.btVoltar.clicked.connect(self.fechar)

    def fechar(self):
        self.close()

    def on_table_view_clicked(self, index):
        # Aqui você pode obter a linha e coluna do índice clicado
        row = index.row()
        # column = index.column()

        # Obtém o texto do item da célula clicada sempre na primeira coluna da linha clicada, que é o nome do programa
        item = self.model.item(row, 0)
        if item is not None:
            cell_text = item.text()
            # print(f"Célula clicada: Linha {row}, Coluna {column}, Texto: {cell_text}")
            self.nome_programa = cell_text
            self.close()


