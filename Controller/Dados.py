import threading
import time
import pandas as pd
from Controller.Pt100PTA9B import PTA9B

class Dado:
    def __init__(self):
        self.PERIODO_PWM = 1.0
        self.PERIODO_PWM_CIRCULACAO_FRIA = 1.0

        self._aciona_buzzer = True
        self._valor_teclado_setpoint_quente = 0
        self._valor_teclado_setpoint_frio = 0

        self.df = pd.read_csv('Controller/db.csv')
        
        self._cursor = 'cross'
        #self._cursor = 'none'
        self._nome_programa = 'Camara choque térmico'
        self._controle_quente_estah_acionado = False
        self._controle_frio_estah_acionado = False
        self._ganho_poporcional_temperatura_quente = 4
        self._temperatura_quente_set_point = 0
        self._temperatura_fria_set_point = 0
        self._pwm_circulacao_fria = 50
        
        
        self._black = '#000000'
        self._white = '#FFFFFF'
        self._brighted = '#C4C4C4'
        self._grey = '#E5E5E5'
        self._grey_dark = "#505050"
        self._red = '#FF0000'
        self._green = '#2CCA28'
        self._blue = '#31455B'

        self.set_temperatura_quente_setpoint(self.df.loc[0,'setpoint_quente'])
        self.set_temperatura_fria_setpoint(self.df.loc[0,'setpoint_frio'])

        self.temp = Temperatura()

        self.temp.start()

    @property
    def aciona_buzzer(self):
        return self._aciona_buzzer
    
    @property
    def valor_teclado_setpoint_quente(self):
        return self._valor_teclado_setpoint_quente
    
    @property
    def valor_teclado_setpoint_frio(self):
        return self._valor_teclado_setpoint_frio
    
    @property
    def cursor(self):
        return self._cursor
    
    @property
    def nome_programa(self):
        return self._nome_programa
    
    @property
    def controle_quente_estah_acionado(self):
        return self._controle_quente_estah_acionado
    
    @property
    def controle_frio_estah_acionado(self):
        return self._controle_frio_estah_acionado
    
    @property
    def ganho_poporcional_temperatura_quente(self):
        return self._ganho_poporcional_temperatura_quente
    
    @property
    def temperatura_quente_set_point(self):
        return self._temperatura_quente_set_point
    
    @property
    def temperatura_fria_set_point(self):
        return self._temperatura_fria_set_point
    
    @property
    def pwm_circulacao_fria(self):
        return self._pwm_circulacao_fria

    
    @property
    def black(self):
        return self._black
    
    @property
    def white(self):
        return self._white
    
    @property
    def brighted(self):
        return self._brighted
    
    @property
    def grey(self):
        return self._grey
    
    @property
    def red(self):
        return self._red
    
    @property
    def green(self):
        return self._green

    @property
    def blue(self):
        return self._blue
    
    def set_temperatura_quente_setpoint(self, setpoint):
        self._temperatura_quente_set_point = setpoint
        self.df.loc[0,'setpoint_quente'] = self._temperatura_quente_set_point
        print(self.df.loc[0,'setpoint_quente'])
        self.df.to_csv('Controller/db.csv', index=False)

    def set_valor_teclado_setpoint_quente(self, setpoint):
        self._valor_teclado_setpoint_quente = setpoint

    def set_temperatura_fria_setpoint(self, setpoint):
        self._temperatura_fria_set_point = setpoint
        self.df.loc[0,'setpoint_frio'] = self._temperatura_fria_set_point
        print(self.df.loc[0,'setpoint_frio'])
        self.df.to_csv('Controller/db.csv', index=False)


    def set_valor_teclado_setpoint_frio(self, setpoint):
        self._valor_teclado_setpoint_frio = setpoint

    def set_pwm_circulacao_fria(self, valor):
        self._pwm_circulacao_fria = valor
        

    
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
