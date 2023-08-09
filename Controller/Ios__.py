#import RPi.GPIO as GPIO
import time
import threading

class InOut:
    def __init__(self):

        self._delay_refrigeracao = Delay(tempo=10)

        self._status_elevador = ''

        self.buzzer(0)
        self.resistencias(0)
        self.circulacao_fria(0)
        self.elevador(0)
        self.refrigeracao(0)
        self.circulacao_quente(0)

        self.PARTE_QUENTE = 1
        self.PARTE_FRIA = 0
    
    def stop(self):
        self._delay_refrigeracao.stop()

        
    def buzzer(self, estado):
        # Ação invertida de controle
        if estado == 1:
            pass
        else:
            pass
            
    def resistencias(self, estado):
        if estado == 1:
            print('Resistencia ligada\n')
        else:
            print('Resistencia desligada\n')

    def circulacao_fria(self, estado):
        if estado == 1:
            pass
        else:
            pass

    def elevador(self, estado):
        # Ação invertida de controle
        if estado == 1:
            #GPIO.output(self.ELEVADOR, 0)
            self._status_elevador = 'quente'
        else:
            #GPIO.output(self.ELEVADOR, 1)
            self._status_elevador = 'frio'

    def refrigeracao(self, estado):
        #delay = Delay()
        # Ação invertida de controle
        if estado == 1:
            if self._delay_refrigeracao._iniciar == False:
                print("ligou frio")
        else:
            self._delay_refrigeracao._iniciar = True
            print("desligou frio")

    def circulacao_quente(self, estado):
        # Ação invertida de controle
        if estado == 1:
            pass
        else:
            pass

    @property
    def protecao_termica(self):
        return 1
    
    @property
    def botao_emergencia(self):
        return 1
    
    @property
    def porta_aberta_fechada(self):
        return 0

    @property
    def status_elevador(self):
        return self._status_elevador
    
class Delay(threading.Thread):
    def __init__(self, tempo = 4):
        threading.Thread.__init__(self)
        self._running = True
        self._tempo = tempo
        self._cnt = 0
        self._iniciar = False
        self.start()

    def run(self) -> None:
        while self._running == True:
            if self._iniciar == True:
                self._cnt+=1
                if self._cnt >= self._tempo:
                    self._cnt = 0
                    self._iniciar = False

            time.sleep(1)

    def stop(self):
        self._running = False
        self.join()

    