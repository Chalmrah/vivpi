try:
  import usocket as socket
except:
  import socket
  
from time import sleep

from machine import Pin, I2C
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

import BME280
import ujson

warmSens = I2C(scl=Pin(22), sda=Pin(21), freq=1000)
coldSens = I2C(scl=Pin(18), sda=Pin(14), freq=1000)

ssid = 'SSID'
password = 'PASSWORD'
staticIP ='IP ADDRESS'
subnet = 'SUBNET'
gateway = 'DEFAULT GATEWAY'
dns = 'DNS SERVER'

station = network.WLAN(network.STA_IF)

station.active(True)
station.ifconfig((staticIP, subnet, gateway, dns))
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())