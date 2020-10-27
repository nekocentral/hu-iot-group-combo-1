import serial
import urllib.request
import time

data = []
i = 0

try:
    ser = serial.Serial("COM3", 9600, timeout=1)
    while True:
        outp = ser.readline()
        nicestring = str(outp).replace("b'", "").replace("\\n","").replace("'","")
        time.sleep(1)
        i += 1
        print("time: ")
        print(i)
        if nicestring != None and nicestring != '':
            print("Heartbeat")
            print(nicestring)
            data.append(float(nicestring))

        if i >= 60:
            gem = (sum(data) / len(data))
            gem = round(gem)
            print("Gem: ")
            print(gem)
            i = 0
            urllib.request.urlopen("https://api.thingspeak.com/update.json?api_key=9VEHLUUPS1PHQ3KR&field1="
                                       +str(gem))
except IOError:
    print("Failed to open PORT")
ser.close()

