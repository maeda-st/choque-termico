import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QDialog

class AlphanumericKeyboard(QDialog):
    def __init__(self, dado=None):
        super().__init__()
        self.dado = dado
        self.setWindowTitle("Teclado Alfanumérico")
        self.layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)
        self.grid_layout = QGridLayout()
        self.buttons = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', '<-', 'OK'
        ]
        positions = [(i, j) for i in range(6) for j in range(8)]
        for position, button in zip(positions, self.buttons):
            row, col = position
            button_obj = QPushButton(button)
            if button == '<-':
                button_obj.clicked.connect(self.on_backspace_click)
            elif button == 'OK':
                button_obj.clicked.connect(self.on_ok_click)
            else:
                button_obj.clicked.connect(lambda state, button=button: self.on_button_click(button))
            self.grid_layout.addWidget(button_obj, row, col)
        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)

    def on_button_click(self, button):
        if button == ' ':
            self.line_edit.setText(self.line_edit.text() + ' ')
        else:
            self.line_edit.setText(self.line_edit.text() + button)

    def on_backspace_click(self):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text[:-1])

    def on_ok_click(self):
        value = self.line_edit.text()
        self.dado.set_valor_teclado_setpoint_quente(value)
        self.close()

class NumericKeyboard(QDialog):
    def __init__(self, dado = None, mode = None):
        super().__init__()
        self.dado = dado
        self.mode = mode
        self.setWindowTitle("Teclado Numérico")
        self.layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)
        self.grid_layout = QGridLayout()
        self.buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '.', '0', '<-','-'
        ]
        positions = [(i, j) for i in range(5) for j in range(3)]
        for position, button in zip(positions, self.buttons):
            row, col = position
            button_obj = QPushButton(button)
            if button == '<-':
                button_obj.clicked.connect(self.on_backspace_click)
            elif button == '.':
                button_obj.clicked.connect(self.on_decimal_click)
            else:
                button_obj.clicked.connect(lambda state, button=button: self.on_button_click(button))
            self.grid_layout.addWidget(button_obj, row, col)
        
        ok_button = QPushButton('OK')
        ok_button.clicked.connect(self.on_ok_click)
        self.grid_layout.addWidget(ok_button, 5, 1, 1, 1)

        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)

    def on_button_click(self, button):
        self.line_edit.setText(self.line_edit.text() + button)

    def on_decimal_click(self):
        current_text = self.line_edit.text()
        if '.' not in current_text:
            self.line_edit.setText(current_text + '.')

    def on_backspace_click(self):
        current_text = self.line_edit.text()
        self.line_edit.setText(current_text[:-1])

    def on_ok_click(self):
        value = self.line_edit.text()
        if self.mode == 'quente':
            self.dado.set_valor_teclado_setpoint_quente(value)
        elif self.mode == 'frio':
            self.dado.set_valor_teclado_setpoint_frio(value)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    numeric_keyboard = NumericKeyboard()
    alphanumeric_keyboard = AlphanumericKeyboard()
    numeric_keyboard.show()
    alphanumeric_keyboard.show()
    sys.exit(app.exec_())
