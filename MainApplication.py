import os

import qtmodern.styles
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QFocusEvent, QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import sys
from TextEditorWidgets import *
from HTML_IO import *


# Custom subclass of QMainWindow to customize the window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setObjectName("TextEditor")
        self.setFixedSize(QSize(600, 425))

        # The path to the currently open file.
        # None means we're making a new file or haven't opened one yet
        self.path = None
        self.changes_since_save = False
        self.initializeUI()

        # Try to access settings in .ini file. If it fails then it doesn't exist, so stick with defaults
        self.settings = QSettings("gui.ini", QSettings.IniFormat)
        try:
            # Geometry
            self.resize(self.settings.value('window_size'))
            self.move(self.settings.value('window_position'))
        except:
            pass

    def initializeUI(self):

        self.updateTitle()
        # self.setMinimumSize(QSize(300, 200))
        # self.setMaximumSize(QSize(600, 400))

        #  ======== Widgets ============
        self.text_editor = TextEdit()
        self.text_editor.selectionChanged.connect(self.update_format)
        self.text_editor.textChanged.connect(self.updateSaveState)
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
        # toolbar.setFloatable(False)
        toolbar.setMovable(False)
        # toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(toolbar)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        #  ======== File Actions ============

        # File Open
        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        toolbar.addAction(open_file_action)

        # File Save
        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)
        toolbar.addAction(save_file_action)

        # File Save As
        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.saveas_file)
        file_menu.addAction(saveas_file_action)
        toolbar.addAction(saveas_file_action)

        toolbar.addSeparator()

        edit_menu = self.menuBar().addMenu("&Edit")

        # Undo
        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.text_editor.undo)
        edit_menu.addAction(undo_action)

        # Redo
        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.text_editor.redo)
        toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Cut
        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.text_editor.cut)
        toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        # Copy
        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.text_editor.copy)
        toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        # Paste
        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.text_editor.paste)
        toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        # Select all
        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.text_editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        format_menu = self.menuBar().addMenu("&Format")


        # Bold
        self.bold_action = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(self.set_font_weight)
        toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        # Italic
        self.italic_action = QAction(QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.text_editor.setFontItalic)
        toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        # Underline
        self.underline_action = QAction(QIcon(os.path.join('images', 'edit-underline.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.text_editor.setFontUnderline)
        toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        # Add font_size_box and connect to text_editor
        self.font_size_box = FontSizeBox()
        self.font_size_box.valueChange.connect(self.text_editor.setFontPointSize)
        toolbar.addWidget(self.font_size_box)

        # Add font_box and connect to text_editor
        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.text_editor.setFont)
        toolbar.addWidget(self.font_box)

        # Add Color picker
        self.color_picker = QColorButton()
        self.color_picker.setIconSize(QSize(16, 16))
        self.color_picker.setIcon(QIcon(os.path.join('images', 'edit-color.png')))
        self.color_picker.colorChanged.connect(self.text_editor.setTextColor)

        toolbar.addWidget(self.color_picker)

        #  ======== StatusBar ============
        self.char_count = CharCountDisplay("0/140")
        self.text_editor.charCountChange.connect(self.char_count.updateCharCount)
        self.text_editor.charCountExceeded.connect(self.char_count.flashRed)
        self.text_editor.charCountExceeded.connect(self.showWarningOnStatusBar)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().addPermanentWidget(self.char_count)

        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.font_box,
            self.font_size_box,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            self.color_picker
        ]

        #  ======== Initialize ============
        self.update_format()
        self.show()

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.font_box.setCurrentFont(self.text_editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        self.font_size_box.setCurrentText(str(int(self.text_editor.fontPointSize())))

        self.italic_action.setChecked(self.text_editor.fontItalic())
        self.underline_action.setChecked(self.text_editor.fontUnderline())
        self.bold_action.setChecked(self.text_editor.fontWeight() == QFont.Bold)

        self.block_signals(self._format_actions, False)

    def showWarningOnStatusBar(self):
        self.statusBar().showMessage("Reached maximum character count", 2500)

    def updateSaveState(self):
        self.changes_since_save = True

    def updateTitle(self):
        if self.path:
            self.setWindowTitle("%s - Weta Coding Challenge 2020" % (os.path.basename(self.path)))
        else:
            self.setWindowTitle("Untitled - Weta Coding Challenge 2020")

    def open_file(self):
        if self.maybeSave():
            file_open(self)

    def save_file(self):
        file_save(self)
        self.changes_since_save = False

    def saveas_file(self):
        file_saveas(self)
        self.changes_since_save = False

    def set_font_weight(self, toggled):
        if toggled:
            self.text_editor.setFontWeight(QFont.Bold)
        else:
            self.text_editor.setFontWeight(QFont.Normal)

    # def change_text_editor_font_size(self, new_value):
    #     font = self.text_editor.font()
    #     font.setPointSize(new_value)
    #     self.text_editor.setFont(font)

    def maybeSave(self):
        if self.changes_since_save:
            dialog = UnsavedChangesDialog(self)
            button = dialog.exec_()

            if button == QMessageBox.Cancel:
                return False
            elif button == QMessageBox.Save:
                return self.save_file()

        return True


    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.maybeSave():
            self.settings.setValue('window_size', self.size())
            self.settings.setValue('window_position', self.pos())
            event.accept()
        else:
            event.ignore()


        # QMainWindow.closeEvent(self, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Text Editor")

    window = MainWindow()
    qtmodern.styles.dark(app)
    app.exec_()
