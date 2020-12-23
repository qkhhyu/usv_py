#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import logging
import logging.handlers

from PyQt5.QtWidgets import QFileDialog, QDialog


def log_config_init():
    files_handle = logging.handlers.TimedRotatingFileHandler('band_tool', when='H', interval=3)
    files_handle.suffix = "%Y%m%d_%H%M%S.log"
    formatter = logging.Formatter('[%(filename)s][%(levelname)s][line:%(lineno)d]%(message)s')
    files_handle.setFormatter(formatter)
    # 添加到日志处理对象集合
    logging.getLogger('').addHandler(files_handle)
    logging.getLogger('').setLevel(logging.INFO)

    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('[%(levelname)s][line:%(lineno)d]%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


class Log(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.main = parent
        log_config_init()

    def update_log(self, msg):
        logging.info('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), msg))

    def update_log_ui(self, color, msg):
        self.main.update_text_browser_log('[%s]<font color=%s>%s</font>' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), color, msg))
        logging.info('[%s]%s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), msg))

    def save_log(self, msg):
        file_path = QFileDialog.getSaveFileName(self, '保存文件', './', 'Text Files(*.txt)')[0]
        if file_path:
            fp = open(file_path, 'w')
            fp.write(msg)
            fp.close()
            logging.info('[%s]save_log' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

    def clear_log(self):
        self.main.clear_text_browser_log()
        logging.info('[%s]clear_log' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

