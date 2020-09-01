import serial
import numpy as np
import threading
s1 = []
s2 = []
hr = ''
bp = ''
spo2 = ''
ptt = ''
t = []
dt = 150
last_read_time = -dt

serialArduino = serial.Serial('COM29', 9600)

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