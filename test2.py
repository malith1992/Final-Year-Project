import os
import sys
import Phara
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Notepad(QWidget):
    filename = ''
    def __init__(self):
        super(Notepad, self).__init__()
        self.setGeometry(100, 100, 800, 480)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Book Digitizer Platform')
        self.pylabel = QLabel('Book Digitizer Platform', self)
        self.pylabel.resize(400, 50)
        self.pylabel.move(200, 25)
        self.pylabel.setFont(QFont('SansSerif', 20, weight=QFont.Bold))

        self.pylabel1 = QLabel('Select the book', self)
        self.pylabel1.resize(200, 32)
        self.pylabel1.move(25, 150)
        self.pylabel1.setFont(QFont('SansSerif', 10))

        pybutton1 = QPushButton('Choose', self)
        pybutton1.resize(200, 32)
        pybutton1.move(200, 150)
        pybutton1.clicked.connect(self.open_folder)

        self.pylabel2 = QLabel(self)
        self.pylabel2.resize(400, 32)
        self.pylabel2.move(450, 150)

        self.pybutton2 = QPushButton('Submit', self)
        self.pybutton2.resize(200, 50)
        self.pybutton2.move(300, 250)
        self.pybutton2.setFont(QFont('SansSerif', 12))

        self.pybutton2.clicked.connect(self.submit)

        self.show()



    def open_folder(self):
        self.filename = QFileDialog.getExistingDirectory(self,'Select Directory')
        self.pylabel2.setText(self.filename)

    def submit(self):
        Phara.main(self.filename)
        print(self.filename)

app = QApplication(sys.argv)
writer = Notepad()
sys.exit(app.exec_())