# picoRing

picoRing is a **battery-free ring input device** for subtle finger input.


![picoRing overview](./pictures/picoring_overview.jpg)
> picoRing design. (a) Photograph and (b) illustration of picoRing. (c) Overview of distributed capacitance arrangement technique which can increase the passive response from the sensor coil by enabling a high inductor at a high frequency. (d) Circuit diagram and signal processing of picoRing, which consists of a ring-shaped passive sensor coil and a wristband-shaped reader coil connected to a reader board including a bridge circuit, vector network analyzer, and PC.


![GUI overview](./pictures/gui_overview.jpg)



## Requirement

- OS: Windows
- DLL: PicoVNA 3 software (install [here](https://www.picotech.com/downloads))

### Python

```
py -3.8-32 -m pip install -r requirements.txt
```

- PicoVNA 2 software
- [python 3.8-**32bit**](https://www.python.org/downloads/windows/)
- [numpy+**mkl**](https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
- [scipy](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
- pandas
- pyqt5
- pyqtgraph
- pywin32
- qdarktheme

[why numpy+mkl?](https://stackoverflow.com/questions/33600302/installing-scipy-in-python-3-5-on-32-bit-windows-7-machine)


### Matlab
- RF Toolbox
- PicoVNA 2 software
- PicoVNA Vector Network Analyzer Toolbox

[install guide](https://github.com/picotech/picosdk-matlab-picovna-vector-network-analyzer-toolbox)


## Usage

```
py -3.8-32 main.py # activate qt viewer
py -3.8-32 main.py -f sample_log/s21_press_ring.npy # replay log data with qt viewer
py -3.8-32 main.py -i setting/default.ini # use the specific setting file
py -3.8-32 main.py -d # start with dark mode

py -3.8-32 test.py -v # test picovna
py -3.8-32 test.py -q # activate qt viewer (test ver.)
py -3.8-32 test.py -m # activate matplotlib viewer (test ver.)

# log message
VNA 10162 Loaded
Result of LoadCal: OK
(close window)
VNA Closed


in matlab
test_animation_matlab
```

## Setting

refer to setting/default.ini

## PicoVNA
- [API](https://www.picotech.com/download/manuals/picovna-vector-network-analyzer-programmers-guide.pdf)
- [Python example](https://github.com/picotech/picosdk-picovna-python-examples)
- [Matlab example](https://github.com/picotech/picosdk-matlab-picovna-vector-network-analyzer-toolbox)

