import os
import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
import Phara


class Notepad(QWidget):
    filename = ''
    def __init__(self):
        super(Notepad, self).__init__()

        self.init_ui()

    def init_ui(self):


        pylabel1 = QLabel('Select the book', self)
        pylabel1.resize(200, 32)
        pylabel1.move(25, 50)

        pybutton1 = QPushButton('Choose', self)
        pybutton1.resize(200, 32)
        pybutton1.move(150, 50)
        pybutton1.clicked.connect(self.open_folder)

        self.pyedit = QLabel(self)
        self.pyedit.resize(400, 32)
        self.pyedit.move(375, 50)
        #self.pyedit.setReadOnly(True)

        pybutton2 = QPushButton('Submit', self)
        pybutton2.resize(200, 50)
        pybutton2.move(350, 150)
        pybutton2.clicked.connect(self.submit)

        self.show()



    def open_folder(self):
        self.filename = QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.pyedit.setText(self.filename)

    def submit(self):
        Phara.main(self.filename)
        print(self.filename)

app = QApplication(sys.argv)
writer = Notepad()
sys.exit(app.exec_())