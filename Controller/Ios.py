from collections.abc import Callable, Iterable, Mapping
from typing import Any
import RPi.GPIO as GPIO
import time
import threading

class InOut:
    def __init__(self):
        
        self.BUZZER = 20
        self.RESISTENCIAS = 26
        self.CIRCULACAO_FRIA = 16
        self.ELEVADOR = 19
        self.REFRIGERACAO = 5
        self.CIRCULACAO_QUENTE = 6

        self.PROTECAO_TERMICA = 12
        self.BOTAO_EMERGENCIA = 13
        self.PORTA_ABERTA_FECHADA = 21
        
        GPIO.setmode(GPIO.BCM) 
        GPIO.setwarnings(False)
        
        GPIO.setup(self.BUZZER, GPIO.OUT)
        GPIO.setup(self.RESISTENCIAS, GPIO.OUT)
        GPIO.setup(self.CIRCULACAO_FRIA, GPIO.OUT)
        GPIO.setup(self.ELEVADOR, GPIO.OUT)
        GPIO.setup(self.REFRIGERACAO, GPIO.OUT)
        GPIO.setup(self.CIRCULACAO_QUENTE, GPIO.OUT)

        GPIO.setup(self.PROTECAO_TERMICA, GPIO.IN)
        GPIO.setup(self.BOTAO_EMERGENCIA, GPIO.IN)
        GPIO.setup(self.PORTA_ABERTA_FECHADA, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        GPIO.output(self.BUZZER, 0)
        GPIO.output(self.RESISTENCIAS, 0)
        GPIO.output(self.CIRCULACAO_FRIA, 0)
        GPIO.output(self.ELEVADOR, 0)
        GPIO.output(self.REFRIGERACAO, 0)
        GPIO.output(self.CIRCULACAO_QUENTE, 0)

        self._delay_refrigeracao = Delay(tempo=10)
    
    def stop(self):
        self._delay_refrigeracao.stop()

        
    def buzzer(self, estado):
        if estado == 1:
            GPIO.output(self.BUZZER, 1)
        else:
            GPIO.output(self.BUZZER, 0)
            
    def resistencias(self, estado):
        if estado == 1:
            GPIO.output(self.RESISTENCIAS, 1)
        else:
            GPIO.output(self.RESISTENCIAS, 0)

    def circulacao_fria(self, estado):
        if estado == 1:
            GPIO.output(self.CIRCULACAO_FRIA, 1)
        else:
            GPIO.output(self.CIRCULACAO_FRIA, 0)

    def elevador(self, estado):
        if estado == 1:
            GPIO.output(self.ELEVADOR, 1)
        else:
            GPIO.output(self.ELEVADOR, 0)

    def refrigeracao(self, estado):
        #delay = Delay()
        if estado == 1:
            if self._delay_refrigeracao._iniciar == False:
                GPIO.output(self.REFRIGERACAO, 1)
        else:
            GPIO.output(self.REFRIGERACAO, 0)
            self._delay_refrigeracao._iniciar = True

    def circulacao_quente(self, estado):
        if estado == 1:
            GPIO.output(self.CIRCULACAO_QUENTE, 1)
        else:
            GPIO.output(self.CIRCULACAO_QUENTE, 0)

    @property
    def protecao_termica(self):
        return GPIO.input(self.PROTECAO_TERMICA)
    
    @property
    def botao_emergencia(self):
        return GPIO.input(self.BOTAO_EMERGENCIA)
    
    @property
    def porta_aberta_fechada(self):
        return GPIO.input(self.PORTA_ABERTA_FECHADA)
    
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

    