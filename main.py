# -*- coding: utf-8 -*-

import os
import sys
import time
from argparse import ArgumentParser
from pathvalidate.argparse import validate_filename_arg, validate_filepath_arg

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from viewer.graph_viewer import *
from viewer.sensor_viewer import *
from viewer.switch_viewer import *
from viewer.slider_viewer import *
from viewer.scroll_viewer import *
from viewer.joystick_viewer import *

from util.qt_vna import *

import qdarktheme


class MainWindow(QMainWindow):

    key_pressed = pyqtSignal(QKeyEvent)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        parser = ArgumentParser()
        parser.add_argument("-i", "--inipath", type=validate_filepath_arg)
        parser.add_argument("-f", "--logpath", type=validate_filepath_arg)
        parser.add_argument("-d", "--dark", help="dark mode",
                            action="store_true")
        options = parser.parse_args()

        _inifile = 'setting/default.ini'
        if options.inipath:
            _inifile = options.inipath

        _logfile = None
        if options.logpath:
            _logfile = options.logpath

        if options.dark:
            qdarktheme.setup_theme()
            pass

        self.setWindowTitle("mRing")
        # self.setWindowFlag(Qt.FramelessWindowHint)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        self.default_font = QFont('Arial', 10)
        self.setFont(self.default_font)

        self.tabs = QTabWidget()
        self.vna = QtVNA(self, inifile=_inifile, logfile=_logfile)
        self.graph_viewer = GraphViewer(self)
        self.sensor_viewer = SensorViewer(
            self, inifile=_inifile, dark_mode=options.dark)
        self.switch_viewer = SwitchViewer(self)
        self.scroll_viewer = ScrollViewer(self, inifile=_inifile)
        self.slider_viewer = SliderViewer(self, inifile=_inifile)
        self.joystick_viewer = JoystickViewer(self, inifile=_inifile)
        self.tabs.addTab(self.vna, "VNA setup")
        self.tabs.addTab(self.graph_viewer, "S21 Graph")
        self.tabs.addTab(self.sensor_viewer, "Sensor status")
        self.tabs.addTab(self.switch_viewer, "Switch test (music player)")
        self.tabs.addTab(self.slider_viewer, "Slider test (video player)")
        self.tabs.addTab(self.scroll_viewer, "Scroll test (paper viewer)")
        self.tabs.addTab(self.joystick_viewer,
                         "Joystick test (game controller)")
        self.tabs.setCurrentIndex(0)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.tabs, 1, 0)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        if options.dark:
            self.setStyleSheet(
                "QMainWindow {color: rgb(30, 30, 30)}"
                "QTabBar::tab {color: rgb(30, 30, 30)}"
                "QTabBar::tab::selected {color: rgb(20, 20, 20)}")
        else:
            self.setStyleSheet(
                "QMainWindow {background-color: rgb(250, 250, 255)}"
                "QTabBar::tab {background-color: rgb(240, 240, 250)}"
                "QTabBar::tab::selected {background-color: rgb(230, 230, 240)}")

        self.key_pressed.connect(self.scroll_viewer.onKeyPressEvent)
        self.key_pressed.connect(self.slider_viewer.onKeyPressEvent)
        self.key_pressed.connect(self.joystick_viewer.onKeyPressEvent)

    def setup(self):
        self.vna.initVNA()
        self.tabs.currentChanged.connect(self.updateViewer)
        self.tabs.setCurrentIndex(1)
        self.vna.s21_signal.connect(self.graph_viewer.updateGraph)
        self.vna.peak_signal.connect(
            self.sensor_viewer.updateSensorState)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.vna.update)
        self.timer.setInterval(10)
        self.timer.start()

    def updateViewer(self, id):
        try:
            self.vna.s21_signal.disconnect()
        except TypeError as e:
            pass

        try:
            self.vna.peak_signal.disconnect()
        except TypeError as e:
            pass

        try:
            self.sensor_viewer.sensor_info_signal.disconnect()
        except TypeError as e:
            pass

        self.sensor_viewer.stopViewer()
        self.switch_viewer.pause()
        self.slider_viewer.pause()
        self.scroll_viewer.pause()
        self.joystick_viewer.pause()

        if id == 0:
            self.statusBar().showMessage('')
        elif id == 1:
            self.vna.s21_signal.connect(self.graph_viewer.updateGraph)
        elif id == 2:
            self.sensor_viewer.startViewer()
        elif id >= 3:
            self.sensor_viewer.startViewer(only_update=True)

        self.vna.peak_signal.connect(
            self.sensor_viewer.updateSensorState)

        if id == 3:
            self.sensor_viewer.sensor_info_signal.connect(
                self.switch_viewer.updateMusicState)
        elif id == 4:
            self.sensor_viewer.sensor_info_signal.connect(
                self.slider_viewer.updateVideoState)
        elif id == 5:
            self.sensor_viewer.sensor_info_signal.connect(
                self.scroll_viewer.updatePaperPos)
            self.scroll_viewer.start()
        elif id == 6:
            self.sensor_viewer.sensor_info_signal.connect(
                self.joystick_viewer.updateJoystickState)
            # self.sensor_viewer.sensor_info_signal.connect(
            #    self.joystick_viewer.updateJoystickFig)

    def keyPressEvent(self, event: QKeyEvent):
        self.key_pressed.emit(event)

    def closeEvent(self, event: QCloseEvent):
        self.vna.stop()
        event.accept()


def main():
    def handler(msg_type, msg_log_context, msg_string):
        pass

    PyQt5.QtCore.qInstallMessageHandler(handler)

    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    main.setup()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
