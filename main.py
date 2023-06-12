import sys
from PyQt5.QtWidgets import QApplication
from Model.MainWindow import MainWindow

from img import logo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())