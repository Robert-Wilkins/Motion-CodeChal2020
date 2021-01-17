import inspect

from PyQt5.QtCore import QFileInfo, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QApplication, QMainWindow, QFormLayout, QLineEdit, QTabWidget, QWidget, QAction
import sys

from pyparsing import unicode


def saveUI(ui):
    # Geometry
    ui.settings.setValue('window_size', ui.size())
    ui.settings.setValue('window_position', ui.pos())

    # Text Editor
    # ui.settings.setValue('editor_content', ui.text_editor.ge())


def restoreUI(ui):
    try:
        # Geometry
        ui.resize(ui.settings.value('window_size'))
        ui.move(ui.settings.value('window_position'))

    except:
        pass


