# gejat van https://www.sigmdel.ca/michel/ha/rpi/temp_sensor_en.html

#!/usr/bin/python
import sys
import Adafruit_DHT
import urllib
import ssl

# parameters
DHT_type    = 11
OneWire_pin = 17
sensor_idx  = 38
url_json    = "https://10.0.0.199/json.htm?username=QVBJ=&password=d3Q3ejVzVFNxWnI5Qk52azBXQWo=&type=command&param=udevice&idx="
verbose     = 1  # set to 1 to print out information to the console 
context = ssl._create_unverified_context()

# read dht11 temperature and humidity
humidity, temperature = Adafruit_DHT.read_retry(DHT_type, OneWire_pin)

# use Domoticz JSON url to update
cmd = url_json  + str(sensor_idx) + "&nvalue=0&svalue=" + str(temperature) + ";" + str(humidity) + ";0"
hf = urllib.urlopen(cmd, context=context)
if verbose > 0:
  print 'Sensor data: temperature = {0:0.1f}C,  humidity =  {1:0.1f}%'.format(temperature, humidity)
  print 'Uploaded to Pi: ' + cmd
  print 'Response: ' + hf.read()
hf.close