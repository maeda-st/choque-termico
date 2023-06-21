import sys
from PyQt5.QtWidgets import QApplication
from Model.Models import MainWindow
from Controller.Dados import Dado
from Controller.Dados import Temperatura
from Controller.Pt100PTA9B import PTA9B

from img import logo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dado = Dado()
    temp_quente = PTA9B(port_name='/dev/ttyUSB0',device_address=1, device_debug=False, res_ofset=12.8)
    # temperatura = Temperatura()
    # temperatura.start()
    window = MainWindow(dado=dado)
    window.show() 
    # Quando fecha a aplicação, destroi a plicação no sistema bem como encerra todas as threads em execução.
    sys.exit([app.exec(), dado.temp.stop(), dado.temp.join(),temp_quente.stop(), temp_quente.join()])