import serial
import numpy as np
import threading
import matplotlib.pyplot as plt
from drawnow import *

s1 = []
s2 = []
hr = '' # heart rate
bp = '' # blood pressure
spo2 = '' 
ptt = ''
t = []
dt = 150
last_read_time = -dt
maxt = 200
mint = 0
plt.ion()
serialArduino = serial.Serial('COM29', 9600)
#pre-load dummy data
for i in range(mint,maxt):
    s1.append(0)
    s2.append(0)
    last_read_time+=dt
    t.append(last_read_time)


def plotValues():
    axs = plt.gca()
    fig = plt.gcf()
    axs.plot(t, s1, color= '#69E73D')
    axs.plot(t, s2, color= '#70EEF2')
    plt.yticks(np.arange(0, 1500, 100))
    plt.xticks(np.arange(mint, maxt, dt))
    axs.set_ylim(0, 1000)
    axs.set_xlabel('time')
    axs.set_ylabel('s1 and s2')
    axs.set_title("HR️: "+hr+"       BP: "+bp+"       SPO2: "+spo2+"       PTT: "+ptt, {
        'color': '#ffd700',
        'fontsize': 17,
        'fontweight': 'bold',

    })
    axs.set_facecolor("#010100")
    fig.set_facecolor("#010100")
    fig.canvas.set_window_title('ECG')
    fig.canvas.toolbar.pack_forget()

# runs in a separate thread to get signals data from arduino
def readSerialData():
    while True:
        while (serialArduino.inWaiting()==0):
            # pass
            print("waiting ...")
        valueRead = serialArduino.readline()
        #check if valid value can be casted
        try:
            valueRead = valueRead.decode('utf-8')
            valueList = valueRead.split(',')
            print(valueRead)
            print(valueList)
            if(len(valueList)) == 6:
                valInt1 = int(valueList[0])
                valInt2 = int(valueList[1])
                global hr
                global bp
                global spo2
                global ptt
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
                        global last_read_time
                        last_read_time+=dt
                        # t.append(last_read_time)
                        # t.pop(0)
                        drawnow(plotValues)
                    else:
                        print ("Invalid! negative number")
                else:
                    print ("Invalid! too large")
            else:
                print ("Corrupted Serial")

        except ValueError:
            print ("Invalid! cannot cast")

arduinoThread = threading.Thread(target=readSerialData)
arduinoThread.start()