#!/usr/bin/python
import Adafruit_DHT
import requests
import base64
import paho.mqtt.client as mqtt
import json

# parameters
DHT_type = 11
GPIO = 17
idx  = 4
host = "ul1.haazen.xyz"
port = 1883
username = str(base64.b64encode(b"API"))
password = str(base64.b64encode(b"wt7z5sTSqZr9BNvk0WAj"))
debug = True  # Laat debug info zien. Indien debug niet gewenst dan deze boolean op False zetten

# Data uitlezen van sensor
humidity, temperature = Adafruit_DHT.read_retry(DHT_type, GPIO)

# Data pushen naar domoticz
client = mqtt.Client()
client.connect(host,port,60)
publish_data = {"idx" : idx, "nvalue" : 0, "svalue" : str(temperature) + ";" + str(humidity) + ";0"}
client.publish("domoticz/in", json.dumps(publish_data))
client.disconnect()


# Trigger IFTTT
if int(temperature) < 20:
  theromastat_aan = requests.get("https://maker.ifttt.com/trigger/Them_aan/with/key/c5KXLXywmNEjSeVJq_obu2")
else:
  theromastat_uit = requests.get("https://maker.ifttt.com/trigger/Them_uit/with/key/c5KXLXywmNEjSeVJq_obu2")

# Debug code
if debug == True:
  print('Sensor data: temperature = {0:0.1f}C,  humidity =  {1:0.1f}%'.format(temperature, humidity), "\n")
