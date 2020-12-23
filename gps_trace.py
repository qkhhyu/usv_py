#!/usr/bin/python3
# -*- coding: utf-8 -*-
# GPS坐标轨迹处理

import time
import math
import random
import os
import pyqtgraph as pg

from PyQt5.QtWidgets import QMainWindow


class GPSTrace(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.main = parent

    def read_trace(self):
        file = open("trace_src.txt", mode='r')
        lines = file.readlines()
        for line in lines:
            self.main.fix_w.append(float(line.split(',')[1].strip('\n')))
            self.main.fix_j.append(float(line.split(',')[0]))

        self.main.fix_w.append(self.main.fix_w[0])
        self.main.fix_j.append(self.main.fix_j[0])

    def clear_trace(self):
        self.main.fix_w = []
        self.main.fix_j = []

    def read_filt_trace(self):
        file = open("trace_filt.txt", mode='r')
        lines = file.readlines()
        for line in lines:
            self.main.fix_w_filt.append(float(line.split('#')[1].split(',')[1].strip('\n')))
            self.main.fix_j_filt.append(float(line.split('#')[1].split(',')[0]))

        self.main.fix_w_filt.append(self.main.fix_w_filt[0])
        self.main.fix_j_filt.append(self.main.fix_j_filt[0])

    def clear_filt_trace(self):
        self.main.fix_w_filt = []
        self.main.fix_j_filt = []
