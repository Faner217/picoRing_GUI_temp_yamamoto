# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import traceback
from threading import Thread, Lock

import numpy as np
import win32com.client
import scipy.signal as sig


class PicoVNA():
    def __init__(self, start_freq=26, freq_step=0.03, step_num=101, input_power=-3, bandwidth=140000):
        # connect to VNA
        self.vna = win32com.client.Dispatch("PicoControl2.PicoVNA_2")
        findVNA = self.vna.FND()
        print('VNA {} loaded'.format(findVNA))

        self.start_freq = start_freq
        self.freq_step = freq_step
        self.step_num = step_num
        self.input_power = input_power
        self.bandwidth = bandwidth

        # load calibration file
        ans = self.vna.LoadCal(
            'calibration_file/25_30_201_140kHz_ncal.cal')
        print("Result of LoadCal: {}".format(ans))

        ans = self.vna.setFreqPlan(self.start_freq,
                                   self.freq_step,
                                   self.step_num,
                                   self.input_power,
                                   self.bandwidth)
        print("Result of setFreqPlan: {}".format(ans))

        self.freq, self.dB, self.phase, \
            self.ave_dB, self.ave_phase, \
            self.std_dB, self.std_phase = \
            None, None, None, None, None, None, None

        self.fps = 0
        self.average(ave_num=10)
        self.setupEnhance()

    def _getRawS21(self):
        self.vna.Measure("S21")
        et = time.time()
        # print("Time to measure S21: {}s".format(et-st))
        raw_dB = self.vna.GetData("S21", "logmag", 0)
        raw_phase = self.vna.GetData("S21", "phase", 0)
        splitdata_dB = raw_dB.split(',')
        converteddata_dB = np.array(splitdata_dB)
        converteddata_dB = converteddata_dB.astype(float)
        splitdata_phase = raw_phase.split(',')
        converteddata_phase = np.array(splitdata_phase)
        converteddata_phase = converteddata_phase.astype(float)
        freq = converteddata_dB[:: 2]/1e6
        dB = converteddata_dB[1:: 2]
        phase = converteddata_phase[1:: 2]
        return freq, dB, phase

    def setupEnhance(self, smoo=1, bw=140000, ave=1):
        time.sleep(0.1)
        ans = self.vna.setEnhance("Smoo", smoo)
        print("Result of setEnhance (Smooth: {}): {}".format(smoo, ans))

        ans = self.vna.setEnhance("BW", bw)
        print("Result of setEnhance (BW: {} kHz): {}".format(bw/1e3, ans))

        ans = self.vna.setEnhance("Aver", ave)
        print("Result of setEnhance (Average cnt. {}): {}".format(ave, ans))
        time.sleep(0.1)

    def getFPS(self):
        return self.fps

    def getS21(self):
        self.freq, self.dB, self.phase = self._getRawS21()
        return self.freq, self.dB, self.phase

    def getDiffS21(self):
        return self.freq, self.dB - self.ave_dB, self.phase - self.ave_phase

    def average(self, ave_num=10):
        time.sleep(0.3)
        dB_arr = np.zeros(shape=(ave_num, self.step_num))
        phase_arr = np.zeros(shape=(ave_num, self.step_num))

        st = time.time()
        for i in range(ave_num):
            freq, dB, phase = self.getS21()
            dB_arr[i] = dB
            phase_arr[i] = phase
        et = time.time()

        self.fps = 1.0/(et-st)*ave_num
        print('VNA get S21: {:.2f}fps'.format(self.fps))

        self.freq = freq
        self.ave_dB = np.average(dB_arr, axis=0)
        self.ave_phase = np.average(phase_arr, axis=0)
        self.std_dB = np.std(dB_arr, axis=0, ddof=1)
        self.std_phase = np.std(phase_arr, axis=0, ddof=1)

    def getBaseS21(self):
        return self.freq, self.ave_dB, self.ave_phase

    def getStdS21(self):
        return self.freq, self.std_dB, self.std_phase

    def __del__(self):
        self.vna.CloseVNA()
        print("VNA Closed")


def main(argv):

    vna = PicoVNA()
    try:
        while True:
            freq, dB, phase = vna.getS21()
            # print('freq: ', freq)
            print('dB: ', dB)
            # print('phase: ', phase)
            time.sleep(0.1)

    except Exception as e:
        del vna
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main(sys.argv)
    sys.exit()
