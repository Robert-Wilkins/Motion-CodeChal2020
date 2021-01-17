import os

from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QKeyEvent, QColor
from PyQt5.QtWidgets import QTextEdit, QComboBox, QLabel, QApplication

# ====================================
#  Text editor Widget
# This widget
# ====================================
class TextEdit(QTextEdit):
    charCountChange = pyqtSignal(int)
    charCountExceeded = pyqtSignal()

    def __init__(self, arg):
        super(TextEdit, self).__init__(arg)
        self.charCount = 0
        self.charLimit = 140
        self.updateCharCount()
        self.textChanged.connect(self.updateCharCount)

    def setFontPointSize(self, size: float):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

    # def setFontWeight(self, p_int):
    #     # current_cursor = self.textCursor()
    #     # self.selectAll()
    #     super(TextEdit, self).setFontWeight(p_int)
    #     # self.setTextCursor(current_cursor)
    #
    # def setFontItalic(self, bool):
    #     # current_cursor = self.textCursor()
    #     # self.selectAll()
    #     super(TextEdit, self).setFontItalic(bool)
    #     # self.setTextCursor(current_cursor)
    #
    # def setFontUnderline(self, bool):
    #     # current_cursor = self.textCursor()
    #     # self.selectAll()
    #     super(TextEdit, self).setFontUnderline(bool)
    #     # self.setTextCursor(current_cursor)

    def updateCharCount(self):
        self.charCount = len(self.toPlainText())
        self.charCountChange.emit(self.charCount)

    def keyPressEvent(self, event: QKeyEvent):
        # if we're safe to add chars or the key press is not a symbol or is a backspace
        if self.charCount < self.charLimit or len(event.text()) != 1 or event.key() == Qt.Key_Backspace:
            # Continue as normal
            super(TextEdit, self).keyPressEvent(event)
        else:
            # else we're trying to add chars that would exceed the limit, so throw error and escape
            self.charCountExceeded.emit()
            return

    # Only working override for dragging in/pasting text
    def insertFromMimeData(self, source: QMimeData):
        # If the thing we're adding will exceed the charCount, throw error and escape
        if len(QApplication.clipboard().text()) + self.charCount > self.charLimit:
            self.charCountExceeded.emit()
            return
        else:
            super(TextEdit, self).insertFromMimeData(source)


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
