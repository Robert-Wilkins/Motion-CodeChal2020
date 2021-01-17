from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QKeyEvent, QColor
from PyQt5.QtWidgets import QTextEdit, QComboBox, QLabel, QApplication, QPushButton, QColorDialog, QMessageBox

arrowKeys = [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]


# ====================================
#  Text editor Widget
# ====================================
class TextEdit(QTextEdit):
    charCountChange = pyqtSignal(int)
    charCountExceeded = pyqtSignal()

    def __init__(self, arg = None):
        super(TextEdit, self).__init__(arg)
        self.char_count = 0
        self.char_limit = 140
        self.updateCharCount()
        self.setPlaceholderText("Edit me!")
        self.setFontPointSize(12)
        self.textChanged.connect(self.updateCharCount)


    def updateCharCount(self):
        self.char_count = len(self.toPlainText())
        self.charCountChange.emit(self.char_count)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in arrowKeys:
            self.selectionChanged.emit()

        # if we're safe to add chars or the key press is not a symbol or is a backspace
        if self.char_count < self.char_limit or len(event.text()) != 1 or event.key() == Qt.Key_Backspace:
            # Continue as normal
            super(TextEdit, self).keyPressEvent(event)
        else:
            # else we're trying to add chars that would exceed the limit, so throw error and escape
            self.charCountExceeded.emit()
            return

    # The only working override for dragging in/pasting text
    def insertFromMimeData(self, source: QMimeData):
        # If the thing we're adding will exceed the charCount, throw error and escape
        if len(QApplication.clipboard().text()) + self.char_count > self.char_limit:
            self.charCountExceeded.emit()
            return
        else:
            super(TextEdit, self).insertFromMimeData(source)


# ====================================
#  Font Size Combo Box Widget
# ====================================
class FontSizeBox(QComboBox):
    valueChange = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.configureFontSizeBox()
        self.last_good = self.currentText()
        self.activated.connect(self.clearFocus)

    def configureFontSizeBox(self):
        list_of_font_sizes = [8, 9, 10, 11, 12, 14, 18, 24, 30, 36, 48, 60, 72, 96]
        for size in list_of_font_sizes:
            self.addItem(str(size))
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setCompleter(None)

    def focusOutEvent(self, focus_event):
        super().focusOutEvent(focus_event)
        self.sanitizeInput()
        self.valueChange.emit(int(self.currentText()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.clearFocus()
        super(FontSizeBox, self).keyPressEvent(event)

    def sanitizeInput(self):
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


# ====================================
#  Number of Characters Display Widget
# ====================================
class CharCountDisplay(QLabel):

    def __init__(self, args):
        super(CharCountDisplay, self).__init__(args)
        self.charCount = 0

        font = self.font()
        font.setBold(True)
        self.setFont(font)

        # Setup animation for when char limit is exceeded
        self.animation = QPropertyAnimation(self, b'color')
        self.animation.setDuration(250)
        self.animation.setLoopCount(2)
        self.animation.setStartValue(self.color)
        self.animation.setEndValue(self.color)
        self.animation.setKeyValueAt(0.5, QColor(255, 0, 0))

    def updateCharCount(self, charCount):
        self.charCount = charCount
        self.setText(str(charCount) + "/140")

    def flashRed(self):
        self.animation.start()

    def getColor(self):
        return self.palette().color(self.foregroundRole())

    def setColor(self, color):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), color)
        self.setPalette(palette)

    color = pyqtProperty(QColor, getColor, setColor)


# ====================================
#  Color picker widget from https://www.mfitzp.com/article/qcolorbutton-a-color-selector-tool-for-pyqt/
# ====================================
class QColorButton(QPushButton):
    ''' Custom Qt Widget to show a chosen color. Left-clicking the button shows the color-chooser, while right-clicking resets the color to None (no-color). '''

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(QColor(self._color))

        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        ''' Show color-picker dialog to select color. Qt will use the native dialog by default. '''
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)


class UnsavedChangesDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Unsaved changes")
        self.setText("You have unsaved changes in this file. Would you like to save now?")
        self.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        self.setIcon(QMessageBox.Question)

