import threading
import time
import pandas as pd
from Controller.Pt100PTA9B import PTA9B

class Dado:
    def __init__(self):
        self.PERIODO_PWM = 1.0
        self.PERIODO_PWM_CIRCULACAO_FRIA = 0.5

        self._aciona_buzzer = True
        self._path_db_csv = "/home/maeda/choque-termico/Controller/db.csv"

        self.df = pd.read_csv(self._path_db_csv)
        
        self._cursor = 'cross'
        #self._cursor = 'none'
        self._nome_programa = 'Camara choque térmico'
        
        self._controle_quente_estah_acionado = False
        self._controle_frio_estah_acionado = False
        self._ganho_poporcional_temperatura_quente = 4

        self._temperatura_quente_set_point = 0
        self._temperatura_fria_set_point = 0
        self._pwm_circulacao_fria = 0

        self.set_temperatura_quente_setpoint(self.df.loc[0,'setpoint_quente'])
        self.set_temperatura_fria_setpoint(self.df.loc[0,'setpoint_frio'])
        self.set_pwm_circulacao_fria(self.df.loc[0,'pwm_circulacao'])

        # Variáveis relativas ao modo automático da tela form_iniciar
        self._nome_programa_ciclo = ''
        self._setpoint_quente_ciclo = 0.0
        self._setpoint_frio_ciclo = 0.0
        self._tempo_parte_quente_ciclo = 0
        self._tempo_parte_fria_ciclo = 0
        self._quantidade_de_ciclo = 0
        self._potencia_ventilador_ciclo = 0
        self._controle_proporcional_ciclo = 0.0
        self._inicio_do_ciclo = ''
        self._estabilizar_temperatura_ciclo = ''
        #------------------------------------------------------------

        self.temp = Temperatura()

        self.temp.start()

    # Variáveis relativas ao modo automático da tela form_iniciar
    '''
    self._nome_programa_ciclo = ''
    self._setpoint_quente_ciclo = 0.0
    self._setpoint_frio_ciclo = 0.0
    self._tempo_parte_quente_ciclo = 0
    self._tempo_parte_fria_ciclo = 0
    self._quantidade_de_ciclo = 0
    self._potencia_ventilador_ciclo = 0
    self._controle_proporcional_ciclo = 0.0
    self._inicio_do_ciclo = ''
    self._estabilizar_temperatura_ciclo = ''
    '''
    @property
    def nome_programa_ciclo(self):
        return self._nome_programa_ciclo
    @property
    def setpoint_quente_ciclo(self):
        return self._setpoint_quente_ciclo
    @property
    def setpoint_frio_ciclo(self):
        return self._setpoint_frio_ciclo
    @property
    def tempo_parte_quente_ciclo(self):
        return self._tempo_parte_quente_ciclo
    @property
    def tempo_parte_fria_ciclo(self):
        return self._tempo_parte_fria_ciclo
    @property
    def quantidade_de_cliclo(self):
        return self._quantidade_de_ciclo
    @property
    def potencia_ventilador_ciclo(self):
        return self._potencia_ventilador_ciclo
    @property
    def controle_proporcional_ciclo(self):
        return self._controle_proporcional_ciclo
    @property
    def inicio_do_ciclo(self):
        return self._inicio_do_ciclo
    @property
    def estabilizar_temperatura_ciclo(self):
        return self._estabilizar_temperatura_ciclo
    
    def set_nome_programa_ciclo(self, nome: str):
        try:
            self._nome_programa_ciclo = str.strip(nome)
        except TypeError as e:
            print(f"Erro no set_nome_programa_ciclo:\n{e}")
    
    def set_setpoint_quente_ciclo(self, setpoint):
        try:
            self._setpoint_quente_ciclo = setpoint
        except ValueError as e:
            print(f"Erro no set_setpoint_quente_ciclo:\n{e}")
    
    def set_setpoint_frio_ciclo(self, setpoint):
        try:
            self._setpoint_frio_ciclo = setpoint
        except ValueError as e:
            print(f"Erro no set_setpoint_frio_ciclo:\n{e}")
    
    def set_tempo_parte_quente_ciclo(self, tempo):
        try:
            self._tempo_parte_quente_ciclo = int(tempo)
        except ValueError as e:
            print(f"Erro no set_tempo_parte_quente_ciclo:\n{e}")

    def set_tempo_parte_fria_ciclo(self, tempo):
        try:
            self._tempo_parte_fria_ciclo = int(tempo)
        except ValueError as e:
            print(f"Erro no set_tempo_parte_fria_ciclo:\n{e}")

    def set_quantidade_de_ciclo(self, quantidade):
        try:
            self._quantidade_de_ciclo = int(quantidade)
        except ValueError as e:
            print(f"Erro no set_quantidade_de_ciclo:\n{e}")

    def set_potencia_ventilador_ciclo(self, potencia: int):
        try:
            self._potencia_ventilador_ciclo = potencia
        except ValueError as e:
            print(f"Erro na função de configuração da potência do ventilador.\n{e}")

    def set_controle_proporcional_ciclo(self, controle: float):
        try:
            self._controle_proporcional_ciclo = controle
        except ValueError as e:
            print(f"Erro ao configurar o controle proporcional.\n{e}")

    def set_inicio_do_ciclo(self, inicio: str):
        try:
            self._inicio_do_ciclo = inicio
        except Exception as e:
            print(f"Erro ao configurar o inicio do ciclo.\n{e}")
        
    def set_estabilizar_temperatura_ciclo(self, valor: str):
        try:
            self._estabilizar_temperatura_ciclo = valor
        except TypeError as e:
            print(f"Erro ao configurar o estabilizar_temperatura_ciclo.\n{e}")


    #------------------------------------------------------------

    @property
    def aciona_buzzer(self):
        return self._aciona_buzzer
    
    @property
    def cursor(self):
        return self._cursor
    
    @property
    def nome_programa(self):
        return self._nome_programa
    
    @property
    def ganho_poporcional_temperatura_quente(self):
        return self._ganho_poporcional_temperatura_quente
    
    @property
    def controle_quente_estah_acionado(self):
        return self._controle_quente_estah_acionado
    
    @property
    def controle_frio_estah_acionado(self):
        return self._controle_frio_estah_acionado
    
    # Controles manual
    @property
    def temperatura_quente_set_point(self):
        return self._temperatura_quente_set_point
    
    @property
    def temperatura_fria_set_point(self):
        return self._temperatura_fria_set_point
    
    @property
    def pwm_circulacao_fria(self):
        return self._pwm_circulacao_fria
    #-----------------------------------------

    def set_nome_programa_ciclo(self, nome_ciclo):
        self._nome_programa_ciclo = nome_ciclo
    
    def set_temperatura_quente_setpoint(self, setpoint):
        self._temperatura_quente_set_point = setpoint
        self.df.loc[0,'setpoint_quente'] = self._temperatura_quente_set_point
        self.df.to_csv(self._path_db_csv, index=False)

    def set_temperatura_fria_setpoint(self, setpoint):
        self._temperatura_fria_set_point = setpoint
        self.df.loc[0,'setpoint_frio'] = self._temperatura_fria_set_point
        self.df.to_csv(self._path_db_csv, index=False)

    def set_pwm_circulacao_fria(self, setpoint):
        self._pwm_circulacao_fria = setpoint
        self.df.loc[0,'pwm_circulacao'] = self._pwm_circulacao_fria
        self.df.to_csv(self._path_db_csv, index=False)

    def set_ganho_proporcional(self, valor):
        quente = self.temperatura_quente_set_point
        quente = quente*(valor/100)
        self._ganho_poporcional_temperatura_quente = self.temperatura_quente_set_point - quente
    
class Temperatura(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._temperatura = 0
        self._temperatura_fria = 0
        self._running = True
        self.device_temperatura_quente =None

    def run(self):
        self.device_temperatura_quente = PTA9B(port_name='/dev/ttyUSB0',device_address=3, device_debug=False, res_ofset=19.4)
        self.device_temperatura_fria = PTA9B(port_name='/dev/ttyUSB0',device_address=1, device_debug=False, res_ofset=19.2)
        while self._running == True:
            time.sleep(1)
            self._temperatura = self.device_temperatura_quente.get_temperature()
            self._temperatura_fria = self.device_temperatura_fria.get_temperature()
            #print(self.temperatura)

    def stop(self):
        self._running = False
        self.join()

    @property
    def temperatura(self):
        return self._temperatura
    
    @property
    def temperatura_fria(self):
        return self._temperatura_fria
