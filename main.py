from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *  # TODO Clean this up

import sys


# Custom subclass of QMainWindow to customize the window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Editor")

        text_editor = QTextEdit("Edit me!")

        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(600, 400))

        # Set the central widget of the Window.
        self.setCentralWidget(text_editor)


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
