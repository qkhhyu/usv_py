#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 画图处理

import time
import math
import random
import pyqtgraph as pg
import numpy as np

from PyQt5.QtWidgets import QMainWindow


class Curve(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.main = parent
        self.angle = 20
        self.win = None
        self.p_src_data = None
        self.curve_r1 = None
        self.scat = None
        self.time_start = 0
        self.count = 0

    def init_trace(self):
        self.win = pg.GraphicsWindow()
        self.win.setBackground('w')
        pg.setConfigOptions(antialias=True)  # 抗锯齿，平滑
        self.win.setWindowTitle('接收曲线')
        return self.win

    def generate_curve(self):
        # 当前坐标曲线
        self.p_pos = self.win.addPlot(title='当前经纬度坐标')
        self.p_pos.addLegend()
        self.p_pos.setLabel('left', "维度", units='°')
        # 实时采集
        self.scatter_A = self.p_pos.plot(x=self.main.Aj, y=self.main.Aw, pen=None,
                                            symbolBrush='b', symbolPen='w', symbol='o', symbolSize=5, name="当前")
        # 原始轨迹
        self.line_fix = self.p_pos.plot(x=self.main.fix_j, y=self.main.fix_w, pen=None,
                                             symbolBrush='b', symbolPen='w', symbol='d', symbolSize=5, name="原始")
        # 过滤轨迹
        self.line_fix_filt = self.p_pos.plot(x=self.main.fix_j_filt, y=self.main.fix_w_filt, pen="r",
                                             symbolBrush='r', symbolPen='w', symbol='t', symbolSize=7, name="过滤")

        # ## Create text object, use HTML tags to specify color/size
        # self.text = pg.TextItem('', anchor=(-0.3, 0.5), angle=0, border='w', fill=(0, 0, 255, 100))
        # self.p_pos.addItem(self.text)
        # # 方向箭头
        # self.arrow = pg.ArrowItem(angle=0, tipAngle=30, baseAngle=0, headLen=30, tailLen=None)
        # self.p_pos.addItem(self.arrow)


        # 速度曲线
        self.p_speed = self.win.addPlot(title='当前速度')
        self.p_speed.setLabel('left', "速度", units='m/s')
        self.line_speed = self.p_speed.plot(y=self.main.speed, pen='b')
        # 航向曲线
        self.p_course = self.win.addPlot(title='当前航向')
        self.p_course.setLabel('left', "航向角", units='°')
        self.line_course = self.p_course.plot(y=self.main.course, pen='b')

        self.win.nextRow()

        # 距离曲线
        self.p_dis = self.win.addPlot(title='距目标点距离')
        self.p_dis.setLabel('left', "距离", units='m')
        self.line_dis = self.p_dis.plot(y=self.main.speed, pen='b')
        # 方位角曲线
        self.p_angle = self.win.addPlot(title='距目标点方位角')
        self.p_angle.setLabel('left', "方位角", units='°')
        self.line_angle = self.p_angle.plot(y=self.main.angle, pen='b')
        # 磁场方位角曲线
        self.p_heading = self.win.addPlot(title='磁场方位角')
        self.p_heading.setLabel('left', "偏离磁北", units='°')
        self.line_heading = self.p_heading.plot(y=self.main.heading, pen='b')
        self.line_cankao1 = self.p_heading.plot(y=self.main.heading_fix1, pen='r')
        self.line_cankao2 = self.p_heading.plot(y=self.main.heading_fix2, pen='r')

    def update_curve(self):
        try:
            # 更新原始轨迹和过滤轨迹
            self.line_fix.setData(x=self.main.fix_j, y=self.main.fix_w)
            self.line_fix_filt.setData(x=self.main.fix_j_filt, y=self.main.fix_w_filt)

            if len(self.main.Aw) < len(self.main.Aj):
                self.main.Aw.append(self.main.Aw[-1])
            elif len(self.main.Aw) > len(self.main.Aj):
                self.main.Aj.append(self.main.Aj[-1])
            else:
                self.scatter_A.setData(x = self.main.Aj, y=self.main.Aw)
            self.line_speed.setData(y=self.main.speed)
            self.line_dis.setData(y=self.main.L)
            self.line_angle.setData(y=self.main.angle)
            self.line_heading.setData(y=self.main.heading)
            self.line_cankao1.setData(y=self.main.heading_fix1)
            self.line_cankao2.setData(y=self.main.heading_fix2)
            self.line_course.setData(y=self.main.course)
        except Exception as e:
            self.main.msg_sig.emit("black", "[ERR_EXCEPTION]%s" % e)

        """
        if self.count <= len(self.main.fix_j_filt) - 1:
            self.count = self.count + 1
        self.scatter_A.setData(x=self.main.fix_j_filt[:self.count], y=self.main.fix_w_filt[:self.count])
        self.text.setPos(self.main.fix_j_filt[self.count - 1], self.main.fix_w_filt[self.count - 1])
        self.text.setText("方位角 %d°" % (self.count*10))
        self.arrow.setPos(self.main.fix_j_filt[self.count - 1], self.main.fix_w_filt[self.count - 1])
        self.arrow.setStyle(angle=(self.count*10 + 90))
        """

