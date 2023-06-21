import minimalmodbus
import time

# slave address (in decimal)
DEVICE_ADDRESS = 1
# ENABLE/DISABLE communication debug mode
DEVICE_DEBUG = True
# Master PORT name -- Change as needed for your host.
PORT_NAME = '/dev/ttyUSB0'

# MODBUS instrument initialization
try:
    instrument = minimalmodbus.Instrument(PORT_NAME, DEVICE_ADDRESS, debug=DEVICE_DEBUG)
except:
    print("Falha na conunicação!")

# MODBUS instrument connection settings
# Change as needed depending on your Hardware requirements
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.mode = minimalmodbus.MODE_RTU
instrument.serial.timeout = 0.2

# Read Temperature
REGISTER_ADDRESS_TEMP = 1
REGISTER_NUMBER_DECIMALS = 1
ModBus_Command = 3

while True:
    # Register number, number of decimals, function code
#    temperature = instrument.read_register(1, 2, 4)
    try:
        temperature = instrument.read_register(REGISTER_ADDRESS_TEMP, REGISTER_NUMBER_DECIMALS, ModBus_Command)
        print(temperature)
        temp_celcius = temperature / 10
    except IOError:
        print("Failed to read from instrument")
    time.sleep(1)