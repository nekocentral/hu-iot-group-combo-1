#!/usr/bin/python
import Adafruit_DHT
import requests
import base64

# parameters
DHT_type = 11
GPIO = 17
idx  = "38"
host = "https://10.0.0.199/"
username = str(base64.b64encode(b"API"))
password = str(base64.b64encode(b"wt7z5sTSqZr9BNvk0WAj"))
debug = True  # Laat debug info zien. Indien debug niet gewenst dan deze boolean op False zetten

# Data uitlezen van sensor
humidity, temperature = Adafruit_DHT.read_retry(DHT_type, GPIO)

# Data pushen naar domoticz
username_url = "json.htm?username=" + username[2:-1]
password_url = "=&password=" + password[2:-1]
url = host + username_url + password_url + "=&type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + str(temperature) + ";" + str(humidity) + ";0"
push_data = requests.get(url, verify=False)

# Debug code
if debug == True:
  print('Sensor data: temperature = {0:0.1f}C,  humidity =  {1:0.1f}%'.format(temperature, humidity), "\n")
  print('Uploaded to Pi: ' + url, "\n")
  print('Response: ' + str(push_data.content))