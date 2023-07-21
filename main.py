import sys
from PyQt5.QtWidgets import QApplication
from Model.Models import MainWindow
from Controller.Dados import Dado
from Controller.ControleProporcional import ControleProporcional, ControleFrio
from Controller.Ios import InOut

from img import logo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dado = Dado()
    io = InOut()
    pwm = ControleProporcional(dado=dado, saida=io)
    pwm_frio = ControleFrio(dado=dado, saida=io)
    #temp_quente = PTA9B(port_name='/dev/ttyUSB0',device_address=1, device_debug=False, res_ofset=8.9)
    # temp_quente = PTA9B(port_name='/dev/ttyUSB0',device_address=1, device_debug=False, res_ofset=19.4)
    # temp_quente = PTA9B(port_name='/dev/ttyUSB0',device_address=1, device_debug=True, res_ofset = -0.2)
    # temperatura = Temperatura()
    # temperatura.start()
    window = MainWindow(dado=dado, io=io)
    window.show()
    # Quando fecha a aplicação, destroi a plicação no sistema bem como encerra todas as threads em execução.
    sys.exit([app.exec(), dado.temp.stop(), pwm.stop(), pwm_frio.stop(), io.stop()])
    #sys.exit([app.exec()])