# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'View/form_operacao_manual.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_formManual(object):
    def setupUi(self, formManual):
        formManual.setObjectName("formManual")
        formManual.resize(1020, 600)
        self.btVoltar = QtWidgets.QPushButton(formManual)
        self.btVoltar.setGeometry(QtCore.QRect(860, 510, 131, 71))
        self.btVoltar.setObjectName("btVoltar")
        self.label = QtWidgets.QLabel(formManual)
        self.label.setGeometry(QtCore.QRect(50, 50, 161, 51))
        self.label.setObjectName("label")
        self.btElevadorSobe = QtWidgets.QPushButton(formManual)
        self.btElevadorSobe.setGeometry(QtCore.QRect(240, 50, 84, 54))
        self.btElevadorSobe.setObjectName("btElevadorSobe")
        self.btElevadorDesce = QtWidgets.QPushButton(formManual)
        self.btElevadorDesce.setGeometry(QtCore.QRect(340, 50, 84, 54))
        self.btElevadorDesce.setObjectName("btElevadorDesce")
        self.label_2 = QtWidgets.QLabel(formManual)
        self.label_2.setGeometry(QtCore.QRect(50, 180, 211, 51))
        self.label_2.setObjectName("label_2")
        self.txTemperatura = QtWidgets.QLineEdit(formManual)
        self.txTemperatura.setGeometry(QtCore.QRect(260, 190, 131, 31))
        self.txTemperatura.setObjectName("txTemperatura")

        self.retranslateUi(formManual)
        QtCore.QMetaObject.connectSlotsByName(formManual)

    def retranslateUi(self, formManual):
        _translate = QtCore.QCoreApplication.translate
        formManual.setWindowTitle(_translate("formManual", "Tela Manual"))
        self.btVoltar.setText(_translate("formManual", "Voltar"))
        self.label.setText(_translate("formManual", "<html><head/><body><p><span style=\" font-size:28pt; font-weight:600;\">Elevador</span></p></body></html>"))
        self.btElevadorSobe.setText(_translate("formManual", "Sobe"))
        self.btElevadorDesce.setText(_translate("formManual", "Desce"))
        self.label_2.setText(_translate("formManual", "<html><head/><body><p><span style=\" font-size:24pt; font-weight:600;\">Temperatura</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    formManual = QtWidgets.QWidget()
    ui = Ui_formManual()
    ui.setupUi(formManual)
    formManual.show()
    sys.exit(app.exec_())
