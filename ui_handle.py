#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal, QRegExp, QDate
from PyQt5.QtGui import QIntValidator, QRegExpValidator

from beidou import Ui_MainWindow


class UiHandle(Ui_MainWindow, QMainWindow):
    state_sig = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    ####################################################################################################################
    # 日志框处理
    def update_text_browser_log(self, str_buf):
        self.textBrowser_log.append(str_buf)

    def clear_text_browser_log(self):
        self.textBrowser_log.setPlainText('')

    def get_text_browser_log(self):
        return self.textBrowser_log.toPlainText()
