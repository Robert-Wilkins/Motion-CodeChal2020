import os

from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QFileDialog, QMessageBox

HTML_EXTENSIONS = ['.htm', '.html']


def splitext(p):
    return os.path.splitext(p)[1].lower()


def dialog_critical(UI, s):
    dlg = QMessageBox(UI)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()


def file_open(UI):
    path, _ = QFileDialog.getOpenFileName(UI, "Open file", "",
                                          "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

    if path == "":
        return
    try:
        with open(path, 'rU') as file:
            text = file.read()

    except Exception as e:
        dialog_critical(UI, str(e))

    else:
        UI.path = path
        # Qt will automatically try and guess the format as txt/html
        UI.text_editor.setText(text)
        UI.updateTitle()


def file_save(UI):
    if UI.path is None:
        # If we do not have a path, we need to use Save As.
        return UI.saveas_file()

    text = UI.text_editor.toHtml() if splitext(UI.path) in HTML_EXTENSIONS else UI.text_editor.toPlainText()

    try:
        with open(UI.path, 'w') as f:
            f.write(text)

    except Exception as e:
        dialog_critical(UI, str(e))


def file_saveas(UI):
    path, _ = QFileDialog.getSaveFileName(UI, "Save file", "",
                                          "HTML documents (*.html);Text documents (*.txt);All files (*.*)")

    if not path:
        # If dialog is cancelled, will return ''
        return

    text = UI.text_editor.toHtml() if splitext(path) in HTML_EXTENSIONS else UI.text_editor.toPlainText()
    if path.split()[-1] != ".html":
        path += ".html"
    try:
        with open(path, 'w') as f:
            f.write(text)

    except Exception as e:
        if path != "":
            dialog_critical(UI, str(e))

    else:
        UI.path = path
        UI.updateTitle()


def file_print(UI):
    dlg = QPrintDialog()
    if dlg.exec_():
        UI.text_editor.print_(dlg.printer())
