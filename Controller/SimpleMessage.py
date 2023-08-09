from PyQt5.QtWidgets import QMessageBox

class SimpleMessageBox:
    def __init__(self, message, icon=QMessageBox.Information, title="Mensagem"):
        self.message_box = QMessageBox()
        self.message_box.setIcon(icon)
        self.message_box.setWindowTitle(title)
        self.message_box.setText(message)

    def addButton(self, text, role):
        self.message_box.addButton(text, role)

    def exec(self):
        return self.message_box.exec_()
