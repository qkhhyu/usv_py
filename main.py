#!/usr/bin/python3
# -*- coding: utf-8 -*-
__verison__ = "1.0.0"
__authour__ = "tianerjun"

import sys
import threading
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem
from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QFileInfo, QSettings, QVariant
from PyQt5.QtGui import QIcon
from serial.tools import list_ports

from ui_handle import UiHandle
from button_handle import BtnHandle
from curve import Curve
from log import Log
from gps_trace import GPSTrace


class MainCode(UiHandle, QMainWindow):
    msg_sig = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        # 原始轨迹buffer
        self.fix_w = []
        self.fix_j = []
        # 过滤轨迹buffer
        self.fix_w_filt = []
        self.fix_j_filt = []

        # 按键处理
        self.button_connect()
        self.btnHandle = BtnHandle(self)

        # GPS轨迹处理
        self.trace = GPSTrace(self)

        # 画图处理
        self.curve = Curve(self)
        self.Aj = []
        self.Aw = []
        self.Bj = []
        self.Bw = []
        self.speed = []
        self.L = []
        self.angle = []
        self.heading = []
        self.heading_fix1 = []
        self.heading_fix2 = []
        self.course = []
        self.timer_update = QTimer(self)
        self.timer_update.timeout.connect(self.curve.update_curve)

        # 日志模块
        self.log = Log(self)

        # 信号绑定
        self.msg_sig.connect(self.log.update_log_ui)

        # 串口检查，定时更新串口设备
        self.ser = None
        self.serial_receive_data = ''
        self.serial_listbox = []
        self.timer_com_port_check = QTimer(self)
        self.timer_com_port_check.timeout.connect(self.find_all_serial_devices)
        self.timer_com_port_check.start(600)

    def button_connect(self):
        self.pushButton_connect.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_connect'))
        self.pushButton_save_log.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_save_log'))
        self.pushButton_clear_log.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_clear_log'))
        self.pushButton_bd_get_trace.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_bd_get_trace'))
        self.pushButton_bd_show_trace.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_bd_show_trace'))
        self.pushButton_bd_hide_trace.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_bd_hide_trace'))
        self.pushButton_bd_show_trace_filt.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_bd_show_trace_filt'))
        self.pushButton_bd_hide_trace_filt.clicked.connect(lambda: self.btnHandle.btn_handle('pushButton_bd_hide_trace_filt'))


    def find_all_serial_devices(self):
        try:
            temp_serial = []
            for com in list_ports.comports():
                str_com = str(com).replace(' - ', ': ').split(' (')[0]
                temp_serial.append(str(str_com))
            for item in temp_serial:
                if item not in self.serial_listbox:
                    self.comboBox_port.addItem(item)
            for item in self.serial_listbox:
                if item not in temp_serial:
                    for i in range(self.comboBox_port.count()):
                        if item == self.comboBox_port.itemText(i):
                            self.comboBox_port.removeItem(i)
            self.serial_listbox = temp_serial
        except Exception as e:
            self.msg_sig.emit("black", "[ERR_EXCEPTION]%s" % e)

    def serial_on_connected_changed(self, is_connected):
        if is_connected:
            self.comboBox_port.setEnabled(False)
            self.comboBox_baudrate.setEnabled(False)
            self.pushButton_connect.setText('关闭串口')
            self.msg_sig.emit("blue", "打开串口")
            if self.ser.is_connected:
                self.ser.on_data_received(self.serial_on_data_received)
        else:
            self.comboBox_port.setEnabled(True)
            self.comboBox_baudrate.setEnabled(True)
            self.pushButton_connect.setText('打开串口')
            self.msg_sig.emit("blue", "关闭串口")

    def serial_on_data_received(self, data):
        self.msg_sig.emit("black", data+'\n')
        data.strip("")
        self.serial_receive_data += data
        temp = data.split(',')
        try:
            for i in temp:
                if '+21' in i:
                    self.Aw.append(float(i.split('+')[1]))

                if '+112' in i:
                    self.Aj.append(float(i.split('+')[1]))

                if i[:6] == 'speed=':
                    self.speed.append(float(i.split('=')[1])*1852/3600)

                if 'L = ' in i:
                    self.L.append(float(i.split(' = ')[1]))

                if 'A = ' in i:
                    self.angle.append(float(i.split(' = ')[1]))

                if 'heading=' in i:
                    self.heading.append(int(i.split('heading=')[1]))
                    self.heading_fix1.append(124)
                    self.heading_fix2.append(304)


                if 'course=' in i:
                    self.course.append(float(i.split('\r\n')[0].split('course=')[1]))

        except Exception as e:
            self.msg_sig.emit("black", "[ERR_EXCEPTION]%s" % e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainCode()
    root_path = QFileInfo(__file__).absolutePath()
    win.setWindowIcon(QIcon(root_path + "/zkxl.ico"))
    win.setWindowTitle("北斗轨迹测试工具_V"+__verison__)
    win.show()
    sys.exit(app.exec_())

