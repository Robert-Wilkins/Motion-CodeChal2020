from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *  # TODO Clean this up

import sys


list_of_font_sizes = [8, 9, 10, 11, 12, 14, 18, 24, 30, 36, 48, 60, 72, 96]


# Custom subclass of QMainWindow to customize the window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("Text Editor")

        # self.setMinimumSize(QSize(300, 200))
        # self.setMaximumSize(QSize(600, 400))

        # Add Widgets
        self.text_editor = QTextEdit("Edit me!")

        # Add clear button and connect to text_editor
        self.button = QPushButton("Clear")
        self.button.clicked.connect(self.text_editor.clear)

        # Add font_size_box and connect to text_editor
        self.font_size_box = QComboBox()
        self.configure_font_size_box()

        # Add font_box and connect to text_editor
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.text_editor.setFont)
        layout = QVBoxLayout()
        layout.addWidget(self.text_editor)
        layout.addWidget(self.button)
        layout.addWidget(self.font_box)
        layout.addWidget(self.font_size_box)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def configure_font_size_box(self):
        for size in list_of_font_sizes:
            self.font_size_box.addItem(str(size))
        self.font_size_box.setEditable(True)
        self.font_size_box.setInsertPolicy(QComboBox.NoInsert)
        self.font_size_box.setCompleter(None)

    # def sanitize


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
