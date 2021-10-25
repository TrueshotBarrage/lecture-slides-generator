from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def breakpoint(text=""):
    popup = QMessageBox()
    popup.setText(f"Breakpoint: {text}")
    popup.exec()


def popup(text):
    popup = QMessageBox()
    popup.setText(f"{text}")
    popup.exec()
