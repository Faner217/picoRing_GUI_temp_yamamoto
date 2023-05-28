# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import traceback

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

from test.test_picovna import *
from util.peak_detector import *


def main(argv):
    vna = PicoVNA()
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 2, 1)
    ax_diff = fig.add_subplot(1, 2, 2)
    ave_graph, = ax.plot([], [], lw=1, ls='--', label='signal w/o peak')
    raw_graph, = ax.plot([], [], lw=1, label='raw signal')
    peak_graph, = ax.plot([], [], 'o', ms=1, label='peak (>0.1 dB)')

    std_in_diff_graph, = ax_diff.plot(
        [], [], lw=1, ls='--', label='standard deviation')
    diff_graph, = ax_diff.plot([], [], lw=1, label='diff')
    peak_in_diff_graph, = ax_diff.plot(
        [], [], 'o', ms=5, label='peak (>0.1 dB)')

    def init():
        ave_graph.set_data([], [])
        raw_graph.set_data([], [])
        peak_graph.set_data([], [])
        diff_graph.set_data([], [])
        peak_in_diff_graph.set_data([], [])
        std_in_diff_graph.set_data([], [])

        _, ave_dB, _ = vna.getBaseS21()
        base_max = np.max(ave_dB)
        base_min = np.min(ave_dB)
        ax.set_ylabel("S21 LogMag (dBm)")
        ax.set_xlabel("Frequency (MHz)")
        ax.legend()
        ax.set_xlim([26, 29])
        ax.set_ylim([base_min - 1, base_max + 1])
        ax_diff.set_ylabel("Diff of S21 LogMag (dBm)")
        ax_diff.set_xlabel("Frequency (MHz)")
        ax_diff.set_xlim([26, 29])
        ax_diff.set_ylim([0.0, 0.5])
        ax_diff.set_yticks(np.arange(0.0, 0.6, 0.1))
        ax_diff.legend()
        ax_diff.grid()

        return ave_graph, raw_graph, peak_graph, diff_graph, peak_in_diff_graph, std_in_diff_graph,

    def animate(i):

        freq, dB, phase = vna.getS21()

        st = time.time()
        peaks, base_dB, diff_dB, _ = detect_peak_with_polyfit(deg=10, thres=0.03, y=dB)
        et = time.time()
        #print('elapsed time of peak deection: {:.2f}ms'.format((et-st)*1e3))
        ave_graph.set_data(freq, base_dB)
        raw_graph.set_data(freq, dB)

        diff_graph.set_data(freq, diff_dB)

        _, std_dB, std_phase = vna.getStdS21()
        std_in_diff_graph.set_data(freq, std_dB)
        if peaks.size:
            print("peak frequecy: ", freq[peaks])
            peak_graph.set_data(freq[peaks], dB[peaks])
            peak_in_diff_graph.set_data(freq[peaks], diff_dB[peaks])
        else:
            peak_graph.set_data([], [])
            peak_in_diff_graph.set_data([], [])

        return ave_graph, raw_graph, peak_graph, diff_graph, peak_in_diff_graph, std_in_diff_graph,

    try:
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=10, interval=10, blit=True)

        def calibrate(val):
            anim.pause()
            print("Calibration ...")
            vna.average(ave_num=50)
            anim.resume()
            print("Calibration done")

        axes = plt.axes([0.85, 0.9, 0.1, 0.05])
        bcalibration = Button(axes, 'Calibrate', color="white")
        bcalibration.on_clicked(calibrate)
        plt.show()

    except Exception as e:
        del vna
        plt.close()
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main(sys.argv)
    sys.exit()
