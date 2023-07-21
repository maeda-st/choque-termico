import time
import minimalmodbus
import threading
import math


class PTA9B(threading.Thread):
    def __init__(self, port_name, device_address, res_ofset = 0.0, device_debug = True, baudrate = 9600, bytesize = 8, parity = 'N', stopbits = 1, mode = 'rtu', timeout = 0.2):
        self.port_name = port_name
        self.device_address =device_address
        self.device_debug = device_debug
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.mode = mode
        self.timeout = timeout
        self.res_ofset = res_ofset

        self.instrument = None
        self.range_temp_positivo = 99.22 # Resistencia do Pt100 a -2 graus ceusius
        
        self.REGISTER_ADDRESS_RES = 1
        self.REGISTER_NUMBER_DECIMALS = 1
        self.ModBus_Command = 3

        threading.Thread.__init__(self)
        self._temperature = 0
        self._running = True

        # MODBUS instrument initialization
        
        try:
            self.instrument = minimalmodbus.Instrument(self.port_name, self.device_address, debug=self.device_debug)
            # MODBUS instrument connection settings
            # Change as needed depending on your Hardware requirements
            self.instrument.serial.baudrate = self.baudrate
            self.instrument.serial.bytesize = self.bytesize
            self.instrument.serial.parity   = self.parity
            self.instrument.serial.stopbits = self.stopbits
            self.instrument.mode = self.mode
            self.instrument.serial.timeout = self.timeout
            # self.start()
        except:
            print("Falha na conunicação!")
    
    def get_temperature(self):
        Gr_y=0.0
        R=0
        Pt=100
        a= -0.580195 * pow(10,-6)
        b= 3.90802 * pow(10,-3)
        c = 0.0
        t=0

        try:
            #resistence = self.instrument.read_register(self.REGISTER_ADDRESS_RES, self.REGISTER_NUMBER_DECIMALS, self.ModBus_Command)
            resistence = 0
            val_media = 50
            for i in range(val_media):
                resistence += self.instrument.read_register(self.REGISTER_ADDRESS_RES, self.REGISTER_NUMBER_DECIMALS, self.ModBus_Command)

            resistence = resistence/val_media
            
            Gr_y = (resistence - self.res_ofset) # Corrige a resistencia
            if Gr_y > self.range_temp_positivo:
                
            
                R = Gr_y
                c = 1-(R/Pt)
                
                sq = pow(b,2)-(4*(a)*c)
                t = ( -b + math.sqrt( sq ) )/(2*a)
                Gr_y = t
            else:
                R = Gr_y
                a_ = (-(-4.2735))*pow(10,-12)*100
                b_ = (-0.580195)*pow(10,-6)
                c_ = ( (-4.2735)*pow(10,-12) ) + ( 3.90802*pow(10, -3) )
                d_ = 1-(R/Pt)
                q_ = ( 2*pow(b_, 3) - 9*a_*b_*c_ + 27*pow(a_, 2)*d_ ) / (27*pow(a_, 3))
                p_ = ( (-pow(b_, 2)) / (3*pow(a_, 2)) ) + ( c_/a_ )
                
                sq = (pow(q_, 2)/4 + pow(p_, 3)/27)
                
                t = ( self.cubic_root( -(q_/2) + math.sqrt(sq) ) ) + ( self.cubic_root( -(q_/2) - math.sqrt(sq) ) - (b_/(3*a_)) )
                Gr_y = t
        except:
            print("Failed to read from instrument")

        return round(Gr_y,1)

    def cubic_root(self, x):
        ret = 0
        if x < 0:
            x = abs(x)
            ret = x ** (1/3) * (-1)
        else:
            ret = x ** (1/3)
        
        return round(ret)

    def run(self):
        # while self._running == True:
        #         self._temperature = self.get_temperature()
        #         print(f'Temperatura: {self.temperature} C')
        #         time.sleep(1)
        pass

    def stop(self):
        self._running = False

    @property
    def temperature(self):
        return self._temperature