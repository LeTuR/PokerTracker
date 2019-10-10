import sys
import random

from PySide2 import QtCore, QtWidgets, QtGui


class Table(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.pixmap = QtGui.QPixmap('C:/Users/acesareh/ProjetPerso/PokerTracker/poker_tracker/gui/color/spade.png')
        self.pixmap = self.pixmap.scaledToHeight(50)
        
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()

        self.label1.setPixmap(self.pixmap)    
        self.label1.setText('A')
        self.label1.setStyleSheet("QLabel { background-color : white; color : Black; }")
        self.font = QtGui.QFont('Calibri', 50)
        self.font.setBold(True)
        self.label1.setFont(self.font)
        
        self.label2.setPixmap(self.pixmap)
        self.label2.setStyleSheet("QLabel { background-color : white;}")
        
        self.layout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.setLayout(self.layout)


class Parent(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.card = Table()
        self.size = (100, 100)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.card)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    test = Parent()
    test.show()
    sys.exit(app.exec_())
