import sys, os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

class project(QDialog):

    def __init__(self):
        super(project,self).__init__()
        loadUi('upload.ui',self)
        self.setWindowTitle('Book upload')
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
    @pyqtSlot()

    def on_pushButton_clicked(self):

        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        with open(filename[0], 'r') as f:
            file_text = f.read()
            self.text.setText(file_text)


app=QApplication(sys.argv)
widget=project()
widget.show()
sys.exit(app.exec_())