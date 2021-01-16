import os

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QFocusEvent, QIcon
from PyQt5.QtWidgets import *  # TODO Clean this up
from PyQt5 import QtCore, QtGui
import sys

from PyQt5.uic.properties import QtGui, QtCore



class FontSizeBox(QComboBox):
    valueChange = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.configure_font_size_box()
        self.last_good = self.currentText()
        # self.font_size = int(self.currentText())
        self.activated.connect(self.clearFocus)
        # self.focusOutEvent.connect(self.sanitize_input)

    def configure_font_size_box(self):
        list_of_font_sizes = [8, 9, 10, 11, 12, 14, 18, 24, 30, 36, 48, 60, 72, 96]
        for size in list_of_font_sizes:
            self.addItem(str(size))
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setCompleter(None)

    def focusOutEvent(self, focus_event):
        super().focusOutEvent(focus_event)
        self.sanitize_input()
        self.valueChange.emit(int(self.currentText()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
        super(FontSizeBox, self).keyPressEvent(event)

    def sanitize_input(self):
        # Remove all whitespace. This will change inputs like "3 3" to "33",
        # but this is the the behavior of the Adobe suite inputs and is an acceptable outcome
        self.setCurrentText(self.currentText().replace(" ", ""))

        # If the textbox contains only numbers we're safe and can update last know good
        if self.currentText().isdecimal():
            self.last_good = self.currentText()
            # Clamp to min/max
            cur_size = int(self.currentText())
            new_size = min(max(cur_size, 4), 128)
            self.setCurrentText(str(new_size))
        else:  # Else it contains something that's not a number, so revert to last know good
            self.setCurrentText(self.last_good)


# Custom subclass of QMainWindow to customize the window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button_is_checked = True

        self.setWindowTitle("Text Editor")

        # self.setMinimumSize(QSize(300, 200))
        # self.setMaximumSize(QSize(600, 400))

        #  ======== Widgets ============
        self.text_editor = QTextEdit("Edit me!")

        # Add clear button and connect to text_editor
        self.button = QPushButton("Clear")
        self.button.clicked.connect(self.text_editor.clear)


        #  ======== Layout ============
        layout = QVBoxLayout()
        layout.addWidget(self.text_editor)
        layout.addWidget(self.button)
        # layout.addWidget(self.font_box)
        # layout.addWidget(self.font_size_box)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

        #  ======== Toolbar + Menu ============
        # Toolbar
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        # toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")


        # Actions
        self.bold_action = QAction(QIcon('/Users/Robert/Programming/Motion-CodeChal2020/edit-bold.png'), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(self.set_font_weight)
        toolbar.addAction(self.bold_action)
        edit_menu.addAction(self.bold_action)

        # Add font_size_box and connect to text_editor
        self.font_size_box = FontSizeBox()
        self.font_size_box.valueChange.connect(self.change_text_editor_font_size)
        toolbar.addWidget(self.font_size_box)

        # Add font_box and connect to text_editor
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.text_editor.setFont)
        toolbar.addWidget(self.font_box)


        #  ======== StatusBar ============
        self.setStatusBar(QStatusBar(self))

    def set_font_weight(self, toggled):
        current_cursor = self.text_editor.textCursor()
        self.text_editor.selectAll()
        if toggled:
            self.text_editor.setFontWeight(QFont.Bold)
        else:
            self.text_editor.setFontWeight(QFont.Normal)
        self.text_editor.setTextCursor(current_cursor)

    def change_text_editor_font_size(self, new_value):
        font = self.text_editor.font()
        font.setPointSize(new_value)
        self.text_editor.setFont(font)


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
