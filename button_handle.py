#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 按键的处理过程

from PyQt5.QtWidgets import QMessageBox, QDialog
from serial_base import Serial


class BtnHandle(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.main = parent

    def btn_handle(self, btn_str):
        # 打开串口
        if btn_str == 'pushButton_connect':
            if self.main.pushButton_connect.text() == '打开串口':
                try:
                    current_serial_str = self.main.comboBox_port.currentText()
                    port = current_serial_str.split(":")[0]
                    baud_rate = str(self.main.comboBox_baudrate.currentText())
                    self.main.ser = Serial(port=port, baud_rate=baud_rate)
                    self.main.ser.connect()
                    self.main.ser.on_connected_changed(self.main.serial_on_connected_changed)
                except Exception as e:
                    self.main.msg_sig.emit("red", "[ERR_EXCEPTION]%s" % e)
            elif self.main.pushButton_connect.text() == '关闭串口':
                self.main.ser.disconnect()
        # 保存日志
        elif btn_str == 'pushButton_save_log':
            self.main.log.save_log(self.main.get_text_browser_log())
        # 清除日志
        elif btn_str == 'pushButton_clear_log':
            self.main.log.clear_log()

            self.main.Aj = []
            self.main.Aw = []
            self.main.Bj = []
            self.main.Bw = []
            self.main.speed = []
            self.main.L = []
            self.main.angle = []
            self.main.heading = []
            self.main.heading_fix1 = []
            self.main.heading_fix2 = []
            self.main.course = []

        # 实时采集曲线
        elif btn_str == 'pushButton_bd_get_trace':
            self.main.curve.init_trace()
            self.main.curve.generate_curve()
            self.main.timer_update.start(500)
        # 显示原始轨迹
        elif btn_str == 'pushButton_bd_show_trace':
            self.main.trace.read_trace()
        # 隐藏原始轨迹
        elif btn_str == 'pushButton_bd_hide_trace':
            self.main.trace.clear_trace()
        # 显示过滤轨迹
        elif btn_str == 'pushButton_bd_show_trace_filt':
            self.main.trace.read_filt_trace()
        # 隐藏过滤轨迹
        elif btn_str == 'pushButton_bd_hide_trace_filt':
            self.main.trace.clear_filt_trace()

