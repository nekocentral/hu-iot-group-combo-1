import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json

# Aanmaken van variablen
timer = 20
PIR = 18
idx = 5
host = "ul1.haazen.xyz"
port = 1883

# GPIO instellen
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR,GPIO.IN)

# Timer loop
while True:
    status = GPIO.input(PIR)
    if status == 1:
        print("motion gedetecteerd. Lamp wordt aangezet")
        timer = 20
        time.sleep(5)
        # MQTT code om lamp aan te zetten in Domoticz
        client = mqtt.Client()
        client.connect(host,port,60)
        publish_data = {"idx" : idx, "nvalue" : 1}
        client.publish("domoticz/in", json.dumps(publish_data))
        client.disconnect()
    else:
        timer -= 5
        time.sleep(5)
        if timer > 5:
            continue
        elif timer <= -1:
            # Code om de lamp uit te zetten
            print("lamp wordt uitgezet")
            client = mqtt.Client()
            client.connect(host,port,60)
            publish_data = {"idx" : idx, "nvalue" : 0}
            client.publish("domoticz/in", json.dumps(publish_data))
            client.disconnect()
            time.sleep(5)
        else:
            timer = -1