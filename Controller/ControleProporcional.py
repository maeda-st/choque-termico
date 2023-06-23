from collections.abc import Callable, Iterable, Mapping
from typing import Any
import minimalmodbus
import time
import threading
import math

class ControleProporcional(threading.Thread):
    def __init__(self, dado, saida):
        threading.Thread.__init__(self)
        self.out = saida
        self._dado = dado
        self.Et=0.0
        self.Mv=0.0
        self.Pb=0.0
        self.ton_pwm = 0.0
        self.toff_pwm = 0.0
            
    def run(self):
        while True:
            if self._dado.controle_quente_estah_acionado == True and self.out.porta_aberta_fechada == 0:
                self.Et = self._dado.temperatura_set_point - self._dado.temp.temperatura
                self.Pb = self._dado.ganho_poporcional_sistema

                if self.Pb < 0.2:
                    self.Pb = 0.2
                
                self.Mv = ( 100 / (self.Pb) ) * self.Et
                if self.Mv < 10:
                    self.Mv = 0
                if self.Mv > 100:
                    self.Mv = 100

                self.aciona_pwm(self.Mv)
                
                self.out.circulacao_quente(1)
                self.out.resistencias(1)
                time.sleep(self.ton_pwm)
                self.out.resistencias(0)
                time.sleep(self.toff_pwm)

                # print(self.Et)
                # print(self.Pb)
                print(self.Mv)


            else:
                self.out.resistencias(0)
                self.out.circulacao_quente(0)
                time.sleep(1)

    def aciona_pwm(self, porcento):
        self.ton_pwm = (porcento * self._dado.PERIODO_PWM)/100
        self.toff_pwm = self._dado.PERIODO_PWM - self.ton_pwm