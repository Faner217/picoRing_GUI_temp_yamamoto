# -*- coding: utf-8 -*-

import os
import sys
import time

import math
import datetime
import numpy as np
import pandas as pd
from configparser import ConfigParser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ScrollViewer(QWidget):

    def __init__(self, parent, inifile='setting/default.ini'):
        super().__init__(parent)
        self.winID = parent.winId()
        self.statusbar = parent.statusBar()

        self.paper = QLabel()

        self.parser = ConfigParser()
        self.parser.read(inifile)
        section = 'mouse'
        self.img_dict = {}
        for key in self.parser[section]:
            if key == 'range':
                continue
            img = QPixmap("./pictures/{}_{}.png".format(section, key))
            self.img_dict[key] = img

        self.scroll_pic = QLabel()
        self.scroll_pic.setPixmap(self.img_dict['none'])

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(
            self.scroll_pic, alignment=Qt.AlignCenter | Qt.AlignTop, stretch=1)
        self.mainLayout.addWidget(
            self.paper, alignment=Qt.AlignCenter, stretch=4)

        self.window_geometry = parent.geometry()
        self.window_w, self.window_h = self.window_geometry.width(
        ), self.window_geometry.height() - 200
        self.original_img = QPixmap("./pictures/yokohama.jpg")
        self.original_img = self.original_img.scaledToWidth(
            int(self.window_w * 2.5 / 4))
        self.img_w, self.img_h = self.original_img.width(), self.original_img.height()

        self.offset_h = 0
        self.scroll_angle_pre = self.scroll_angle_now = None
        self.current_angle = 0
        self.current_img = self._renewCropImg()

        self.is_paused = False
        self.scroll_counter = 0
        self.setLayout(self.mainLayout)

    def updatePaperPos(self, sensor_info):
        if self.is_paused:
            return

        scroll_state = sensor_info['mouse']
        self.statusbar.showMessage('scroll state: {}'.format(scroll_state))

        if scroll_state == 'press' or scroll_state == 'none':
            return

        self.scroll_pic.setPixmap(self.img_dict[scroll_state])

        # self.scroll_angle_now = int(scroll_state)
        # if self.scroll_angle_pre == None:
        #     self.scroll_angle_pre = self.scroll_angle_now
        #     return
        #
        # if self.scroll_angle_now == 0 and self.scroll_angle_pre == 90:
        #     diff_angle = 45
        # elif self.scroll_angle_now == 90 and self.scroll_angle_pre == 0:
        #     diff_angle = -45
        # else:
        #     diff_angle = self.scroll_angle_now - self.scroll_angle_pre
        # self.offset_h = self.offset_h + 5 * diff_angle
        # self.scroll_angle_pre = self.scroll_angle_now

        if scroll_state == 'up':
            if self.scroll_counter > 2:
                self.offset_h = self.offset_h - 200
                self.scroll_counter = 0
            else:
                self.scroll_counter = self.scroll_counter + 1
        elif scroll_state == 'down':
            if self.scroll_counter > 2:
                self.offset_h = self.offset_h + 200
                self.scroll_counter = 0
            else:
                self.scroll_counter = self.scroll_counter + 1

        self._renewCropImg()

    def pause(self):
        self.is_paused = True

    def start(self):
        self.is_paused = False

    def _renewCropImg(self):
        self._renewOffsetH()
        cropped_area = QRect(
            0, self.offset_h, self.window_w, self.window_h)
        self.current_img = self.original_img.copy(cropped_area)
        self.paper.setPixmap(self.current_img)

    def _renewOffsetH(self):
        self.offset_h = self.offset_h if self.offset_h + \
            self.window_h < self.img_h else self.img_h - self.window_h
        self.offset_h = self.offset_h if self.offset_h >= 0 else 0

    @pyqtSlot(QKeyEvent)
    def onKeyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_K:
            self.offset_h = self.offset_h - 500
        elif event.key() == Qt.Key_J:
            self.offset_h = self.offset_h + 500
        elif event.key() == Qt.Key_Space:
            self.offset_h = 0

        self._renewCropImg()

        event.accept()
