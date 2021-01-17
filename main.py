import os

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QFocusEvent, QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import sys
from TextEditorWidgets import *
from SaveAndRestore import *


# Custom subclass of QMainWindow to customize the window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setObjectName("TextEditor")
        self.initialize_UI()

        self.settings = QSettings("gui.ini", QSettings.IniFormat)

        restoreUI(self)

    def initialize_UI(self):

        self.setWindowTitle("Text Editor")

        # self.setMinimumSize(QSize(300, 200))
        # self.setMaximumSize(QSize(600, 400))

        #  ======== Widgets ============
        self.text_editor = TextEdit("Edit me!")

        # Add clear button and connect to text_editor
        self.button = QPushButton("Clear")
        self.button.clicked.connect(self.text_editor.clear)

        #  ======== Layout ============
        layout = QVBoxLayout()
        layout.addWidget(self.text_editor)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

        #  ======== Toolbar + Menu ============
        # Toolbar
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        # toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        edit_menu = menu.addMenu("&Edit")

        #  ======== Actions ============

        # Bold
        self.bold_action = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(self.set_font_weight)
        toolbar.addAction(self.bold_action)
        edit_menu.addAction(self.bold_action)

        # Italic
        self.italic_action = QAction(QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.text_editor.setFontItalic)
        toolbar.addAction(self.italic_action)
        edit_menu.addAction(self.italic_action)

        # Underline
        self.underline_action = QAction(QIcon(os.path.join('images', 'edit-underline.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.text_editor.setFontUnderline)
        toolbar.addAction(self.underline_action)
        edit_menu.addAction(self.underline_action)

        # Add font_size_box and connect to text_editor
        self.font_size_box = FontSizeBox()
        self.font_size_box.valueChange.connect(self.text_editor.setFontPointSize)
        toolbar.addWidget(self.font_size_box)

        # Add font_box and connect to text_editor
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.text_editor.setFont)
        toolbar.addWidget(self.font_box)

        #  ======== StatusBar ============
        self.char_count = CharCountDisplay("0/140")
        self.text_editor.charCountChange.connect(self.char_count.updateCharCount)
        self.text_editor.charCountExceeded.connect(self.char_count.flashRed)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().addPermanentWidget(self.char_count)

        #  ======== Initialize ============
        self.show()

    def set_font_weight(self, toggled):
        if toggled:
            self.text_editor.setFontWeight(QFont.Bold)
        else:
            self.text_editor.setFontWeight(QFont.Normal)

    # def change_text_editor_font_size(self, new_value):
    #     font = self.text_editor.font()
    #     font.setPointSize(new_value)
    #     self.text_editor.setFont(font)

    def closeEvent(self, event):
        saveUI(self)
        QMainWindow.closeEvent(self, event)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("Text Editor")

    window = MainWindow()
    app.exec_()
