import serial
import numpy as np
import threading
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
windowWidth = 300
s1 = []
s2 = []
hr = '' # heart rate
bp = '' # blood pressure
spo2 = '' 
ptt = ''
ptr = - windowWidth
serialArduinoA = serial.Serial('COM29', 9600)
serialArduinoB = serial.Serial('COM17', 9600)
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
curve = p.plot(pen=pg.mkPen('#69E73D', width=1))                        # create an empty "plot" (a curve to plot)
curve2 = p.plot(pen=pg.mkPen('#70EEF2', width=1))
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
    timeafter = time.time()
    print("*** elapsed seconds = " + str(timeafter - timenow))

while True:
    if (serialArduinoA.inWaiting()==0 ):
        print("No data from A")
        print("A isOpen= ", str(serialArduinoA.isOpen()))
    if (serialArduinoB.inWaiting()== 0):
        print("No data from B")
        print("B isOpen= ", str(serialArduinoB.isOpen()))
    valueReadA = serialArduinoA.readline() if serialArduinoA.inWaiting() != 0 else ''.encode('utf-8')
    valueReadB = serialArduinoB.readline() if serialArduinoB.inWaiting() != 0 else ''.encode('utf-8')
    #check if valid value can be casted
    try:
        print ("starting ...")
        valueReadA = valueReadA.decode('utf-8')
        valueListA = valueReadA.split(',')
        print(valueReadA)
        print(valueListA)
        valueReadB = valueReadB.decode('utf-8')
        valueListB = valueReadB.split(',')
        print(valueReadB)
        print(valueListB)
        if(len(valueListA)) == 2:
            valInt1 = int(valueListA[0])
            valInt2 = int(valueListA[1].replace('\r\n', '') )
            if valInt1 <= 1500 and valInt2 <= 1500:
                if valInt1 >= 0 and valInt2 >= 0:
                    s1.append(valInt1)
                    s2.append(valInt2)
                    s1.pop(0)
                    s2.pop(0)
        if(len(valueListB)) == 4:    
            hr = valueListB[0]
            bp = valueListB[1]
            spo2 = valueListB[2]
            ptt = valueListB[3].replace('\r\n', '')    # necessary in last val in the valueList
        plotValues()
    except ValueError:
        print ("Invalid! cannot cast")

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################