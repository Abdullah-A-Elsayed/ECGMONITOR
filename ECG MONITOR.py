import serial
import numpy as np
import threading
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
windowWidth = 150
s1 = []
s2 = []
hr = '' # heart rate
bp = '' # blood pressure
spo2 = '' 
ptt = ''
ptr = - windowWidth
serialArduino = serial.Serial('COM10', 9600)
### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################
### pre-load dummy data ###
# s1 = np.linspace(0,0,windowWidth)
# s2 = np.linspace(0,0,windowWidth)
s1 = [0 for x in range (0 , windowWidth+1)]
s2 = [0 for x in range (0 , windowWidth+1)]

### defining window and plots ###
win = pg.GraphicsWindow(title="ECG") # creates a window
win.setWindowFlag(QtCore.Qt.FramelessWindowHint)
win.showMaximized()
p = win.addPlot()  # creates empty space for the plot in the window
curve = p.plot(pen=pg.mkPen('#69E73D', width=2))                        # create an empty "plot" (a curve to plot)
curve2 = p.plot(pen=pg.mkPen('#70EEF2', width=2))
p.hideAxis('bottom')
p.hideAxis('left')
titleHtml = '''
    <br/><br/>
        <div style="font-size:18px; border: 1px solid white">
            <div>
                <span style='color:#70EEF2'><b><span style="color:red; font-size:22px">🩸</span> Blood Pressure:</b></span> <span style="color:white"><b>{}</b></span>
                <br/>
                <span style='color:red'><b><span style="color:red; font-size:22px">❤</span> Heart R️ate:</b></span> <span style="color:white"><b>{}</b></span>
                <span style='color:#69E73D'><b><span style="color:red; font-size:22px"> 💉</span> SPO2:</b></span> <span style="color:white"><b>{}</b></span>
            </div>
            <div>
                <span style='color:#F7F739'><b><span style="color:red; font-size:22px">🕓</span> Pulse Transient Time:</b></span> <span style="color:white"><b>{}</b></span>
            </div>
        </div>
    '''
def plotValues():
    timenow = time.time()
    global curve, curve2, ptr, p
    p.setTitle(title=titleHtml.format(hr, bp, spo2, ptt))
    ptr += 1                              # update x position for displaying the curve
    curve.setData(s1)                     # set the curve with this data
    curve2.setData(s2)                     # set the curve with this data
    curve.setPos(ptr,0)                   # set x position in the graph to 0
    curve2.setPos(ptr,0)                   # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # you MUST process the plot now
    
    # axs.set_title("HR️: "+hr+"       BP: "+bp+"       SPO2: "+spo2+"       PTT: "+ptt, {
    #     'color': '#ffd700',
    #     'fontsize': 17,
    #     'fontweight': 'bold',

    # })
    timeafter = time.time()
    print("*** elapsed seconds = " + str(timeafter - timenow))

while True:
    while (serialArduino.inWaiting()==0):
        # pass
        print("waiting ...")
    
    valueRead = serialArduino.readline()
    #check consumed time
    # timenow = timeafter
    #check if valid value can be casted
    try:
        valueRead = valueRead.decode('utf-8')
        valueList = valueRead.split(',')
        print(valueRead)
        print(valueList)
        if(len(valueList)) == 6:
            valInt1 = int(valueList[0])
            valInt2 = int(valueList[1])
            hr = valueList[2]
            bp = valueList[3]
            spo2 = valueList[4]
            ptt = valueList[5].replace('\r\n', '')    # necessary in last val in the valueList
            # print (bp)
            # print (ptt+"****")
            if valInt1 <= 1500 and valInt2 <= 1500:
                if valInt1 >= 0 and valInt2 >= 0:
                    s1.append(valInt1)
                    s2.append(valInt2)
                    s1.pop(0)
                    s2.pop(0)
                    plotValues()
                else:
                    print ("Invalid! negative number")
            else:
                print ("Invalid! too large")
        else:
            print ("Corrupted Serial")

    except ValueError:
        print ("Invalid! cannot cast")

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################