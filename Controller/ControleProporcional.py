import time
import threading

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
        self._running = True
        self._delay_refrigeracao = 4
        
        self.start()
            
    def run(self):
        while self._running == True:
            if self._dado.controle_quente_estah_acionado == True:
            #if self._dado.controle_quente_estah_acionado:
                self.Et = self._dado.temperatura_quente_set_point - self._dado.temp.temperatura
                self.Pb = self._dado.ganho_poporcional_temperatura_quente

                if self.Pb < 0.2:
                    self.Pb = 0.2
                
                self.Mv = ( 100 / (self.Pb) ) * self.Et
                if self.Mv < 10:
                    self.Mv = 0
                if self.Mv > 100:
                    self.Mv = 100
                
                self.out.circulacao_quente(1)
                self.aciona_pwm(self.Mv)
                if self.out.porta_aberta_fechada == 1:
                    self.out.resistencias(1)
                    time.sleep(self.ton_pwm)
                    self.out.resistencias(0)
                    time.sleep(self.toff_pwm)
                    print(self.Mv)
                else:
                    self.out.resistencias(0)
                    self.out.circulacao_quente(0)
                    #self._dado.controle_quente_estah_acionado = False

                # print(self.Et)
                # print(self.Pb)
                # print(self.Mv)


            else:
                self.out.resistencias(0)
                self.out.circulacao_quente(0)
                time.sleep(1)

    def stop(self):
        self._running = False
        self.join()

    def aciona_pwm(self, porcento):
        self.ton_pwm = (porcento * self._dado.PERIODO_PWM)/100
        self.toff_pwm = self._dado.PERIODO_PWM - self.ton_pwm

class ControleFrio(threading.Thread):
    def __init__(self, dado, saida):
        threading.Thread.__init__(self)
        self.out = saida
        self._dado = dado
        self.ton_pwm_circulacao_fria = 0.0
        self.toff_pwm_circulacao_fria = 0.0
        self._running = True
        
        self.start() 
            
    def run(self):
        while self._running == True:
            if self._dado.controle_frio_estah_acionado == True:
                
                self.aciona_pwm_circulacao_fria(self._dado.pwm_circulacao_fria)

                if self._dado.temperatura_fria_set_point <= self._dado.temp.temperatura_fria:
                    self.out.refrigeracao(1)
                else:
                    self.out.refrigeracao(0)


                self.out.circulacao_fria(1)
                time.sleep(self.ton_pwm_circulacao_fria)
                self.out.circulacao_fria(0)
                time.sleep(self.toff_pwm_circulacao_fria)

            else:
                self.out.circulacao_fria(0)
                self.out.refrigeracao(0)
                time.sleep(1)

    def stop(self):
        self._running = False
        self.join()

    def aciona_pwm_circulacao_fria(self, porcento):
        self.ton_pwm_circulacao_fria = (porcento * self._dado.PERIODO_PWM_CIRCULACAO_FRIA)/100
        self.toff_pwm_circulacao_fria = self._dado.PERIODO_PWM_CIRCULACAO_FRIA - self.ton_pwm_circulacao_fria