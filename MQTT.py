import network
import time
import simple
from simple import MQTTClient
import machine
from machine import Pin, unique_id, PWM, ADC
import ubinascii


led1 = Pin(4, Pin.OUT)


class MQTTClass:
  _mqtt_server = 'broker.hivemq.com'
  _unique_id = ubinascii.hexlify(unique_id())
  
  def _sub_cb(self, topic, message):
    print("PRIMLJENA PORUKA: ",topic, " value: ", message)
    
    


  def __init__(self):
    self.mqtt_conn = MQTTClient(client_id=self._unique_id, server=self._mqtt_server, user='', password='', port=1883)
    self.__wifi_connect()
    self.mqtt_conn.set_callback(self._sub_cb)
    self.mqtt_conn.connect()
    print('Connected to {0} MQTT broker'.format(self._mqtt_server))



  
  def __wifi_connect(self):
    print("Connecting to WiFi", end="")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Wokwi-GUEST", "")
    while not wlan.isconnected():
      print(".", end="")
      time.sleep(0.1)
    print(" Connected!")
    print(wlan.ifconfig())
    




  def sub(self, tema):
    self.mqtt_conn.subscribe(tema)

  