from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *  # TODO Clean this up

import sys

def do_something():
    print("Clicked!")


# Custom subclass of QMainWindow to customize the window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("Text Editor")

        # self.setMinimumSize(QSize(300, 200))
        # self.setMaximumSize(QSize(600, 400))

        self.text_editor = QTextEdit("Edit me!")
        self.text_editor.setFont(QFont("Al Nile"))
        self.button = QPushButton("Clear")

        self.button.clicked.connect(self.text_editor.clear)
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.text_editor.setFont)
        self.font_box.currentFontChanged.connect(self.font_box.currentFont)
        layout = QVBoxLayout()
        layout.addWidget(self.text_editor)
        layout.addWidget(self.button)
        layout.addWidget(self.font_box)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
