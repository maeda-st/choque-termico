import threading
import time
import random

class Dado:
    def __init__(self):
        self.TELA_PRINCIPAL = 0

        self.tela_ativa = self.TELA_PRINCIPAL
        self.aciona_buzzer = True
        self.valor_teclado = None
        
        self._cursor = 'cross'
        #self._cursor = 'none'
        self._nome_programa = 'Camara choque térmico'
        
        self._black = '#000000'
        self._white = '#FFFFFF'
        self._brighted = '#C4C4C4'
        self._grey = '#E5E5E5'
        self._grey_dark = "#505050"
        self._red = '#FF0000'
        self._green = '#2CCA28'
        self._blue = '#31455B'

        self.temp = Temperatura()

        self.temp.start()
    
        
    @property
    def cursor(self):
        return self._cursor
    
    @property
    def nome_programa(self):
        return self._nome_programa

    
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
    
class Temperatura(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._temperatura = 0
        self._running = True

    def run(self):
        cnt = 0
        while self._running == True:
            time.sleep(1)
            self._temperatura = random.randint(20,100)
            #print(self.temperatura)

    def stop(self):
        self._running = False

    @property
    def temperatura(self):
        return self._temperatura
