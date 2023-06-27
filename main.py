import time
import machine
from machine import ADC, PWM, Pin
import MQTT
from MQTT import MQTTClass
import servo
from servo import Servo
import display
from display import Display
import wiegand
from wiegand import Wiegand

### PINOVI KOJI SE KORISTE ###
# 0 taster
# 4 Zeleni LED
# 7 Wiegand Pin1
# 8 Wiegand Pin2
# 11 Crvena LED
# 12 SERVO




############## MQTT BROKER TEME  ##################
# Napisati ispravno ime teme
TEMAPARKING = 'uslvabc/led1'
TEMAPOT = 'uslvabc/pot'

parkingSize = 50 # Broj parking mjesta
allowedUsersList = ["AB EF", "2C CB"] # Primjer
currentUsersList = ["AB EF", "2C CB"] # Primjer

#def motora
servoMotor = Servo(pin=12)

#MQTTClient = MQTTClass()
taster = Pin(0, Pin.IN)

###################### WIEGAND DEFINICIJA #########################
#Ovo ce bit allowedUsersList treba u metodi on_card izmijeniti ime
VALID_FACILITY_CODES = [ '123']
VALID_CARDS = [ '12345' ]

#TESTNI LEDOVI / dodati pinove
GREEN_LED = Pin(4, Pin.OUT)
RED_LED = Pin(11, Pin.OUT)

# PINOVI ZA RFID / Uzeti dva pina na kojima ce biti prekidi / ne slati pin nego broj pina
WIEGAND_ZERO = 7  # Broj pina XX 
WIEGAND_ONE = 8   # Broj pina YY

######################## CALLBACK FUNKCIJA / POZIVA SE PRI OČITANJU ########################
# Ovo treba izmijeniti da otvara/zatvara rampu, salje MQTT poruku, update-a displej
# i pali crvenu/zelenu lampicu
def on_card(card_number, facility_code, cards_read):
	if (card_number in VALID_CARDS) and (facility_code in VALID_FACILITY_CODES):
		GREEN_LED.value(1)
		RED_LED.value(0)
		servoMotor.openRamp()
	else:
	    RED_LED.value(1)
		GREEN_LED.value(0)
    
## READER INICIJALIZACIJA (POSJEDUJE AUTOMATSKI PREKID NE TREBA NISTA RUCNO CITATI)
Wiegand(WIEGAND_ZERO, WIEGAND_ONE, on_card)

# Subscribe na temu 
#MQTTClient.sub(TEMAPARKING)

DisplayObject = Display()


# Ovaj while se nece puno mijenjati samo treba citati mqtt i mozda displej postavljati
# I to mozda na timer staviti
while 1:
  #MQTTClient.mqtt_conn.check_msg()
  time.sleep(0.02)
  
  
