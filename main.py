import time
import machine
from machine import ADC, PWM, Pin, Timer
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

# 12 Zelena LED
# 13 Plava LED
# 14 Crvena LED
# _TFT_DC_PIN = 15
# _TFT_MISO_PIN = 16
# _TFT_CS_PIN = 17
# _TFT_CLK_PIN = 18
# _TFT_MOSI_PIN = 19
# _TFT_RST_PIN = 20

# 21 SERVO
# 22 LED

# 27 Wiegand Pin1
# 28 Wiegand Pin2


############## MQTT BROKER TEME  ##################
# Napisati ispravno ime teme
TEMAPARKING = 'uslvabc/led1'
TEMAPOT = 'uslvabc/pot'

parkingSize = 50 # Broj parking mjesta
allowedUsersList = ["AB EF", "2C CB"] # Primjer
currentUsersList = ["AB EF", "2C CB"] # Primjer

#def motora
servoMotor = Servo(pin=21)

#MQTTClient = MQTTClass()
taster = Pin(0, Pin.IN)

###################### WIEGAND DEFINICIJA #########################
#Ovo ce bit allowedUsersList treba u metodi on_card izmijeniti ime
VALID_FACILITY_CODES = [ 67 ]
VALID_CARDS = [ 41668]

#TESTNI LEDOVI / dodati pinove
GREEN_LED = Pin(12, Pin.OUT)
RED_LED = Pin(14, Pin.OUT)
BLUE_LED = Pin(13, Pin.OUT)

RFIDLED = Pin(22, Pin.OUT)


BLUE_LED.value(0)
GREEN_LED.value(0)
RED_LED.value(0)

# PINOVI ZA RFID / Uzeti dva pina na kojima ce biti prekidi / ne slati pin nego broj pina
WIEGAND_ZERO = 27  # Broj pina XX 
WIEGAND_ONE = 28   # Broj pina YY

DisplayObject = Display()

scanningBool = False


 
def _returnTrue(timer):
    global scanningBool
    scanningBool = False
    print("radi nesto\n")
######################## CALLBACK FUNKCIJA / POZIVA SE PRI OČITANJU ########################
# Ovo treba izmijeniti da otvara/zatvara rampu, salje MQTT poruku, update-a displej
# i pali crvenu/zelenu lampicu
def on_card(card_number, facility_code, cards_read):
    global scanningBool, _returnTrue
    
    if scanningBool == True:
        print(scanningBool, "aa")
        return
    scanningBool = True
    timerMain = Timer(-1)
    timerMain.init(mode=Timer.ONE_SHOT, period=200, callback=_returnTrue)
    if (card_number in VALID_CARDS) and (facility_code in VALID_FACILITY_CODES):
        
        GREEN_LED.value(1)
        RED_LED.value(0)
        RFIDLED.value(1)
        DisplayObject.display_ok()
        print("USPJESNO PROCITANA")
        servoMotor.openRamp()
    else:
        print(int(card_number), "aaa")
        print(int(facility_code), "facility")
        RED_LED.value(1)
        GREEN_LED.value(0)
        RFIDLED.value(0)
        DisplayObject.display_error()
        print("NESTO PROCITANO")
        #DisplayObject.display_error()
    
## READER INICIJALIZACIJA (POSJEDUJE AUTOMATSKI PREKID NE TREBA NISTA RUCNO CITATI)
Wiegand(WIEGAND_ZERO, WIEGAND_ONE, on_card)

# Subscribe na temu 
#MQTTClient.sub(TEMAPARKING)


#DisplayObject.display_ok()




#RFIDLED.value(0)
#print("servo pokrenut")
#time.sleep(2)
#servoMotor.openRamp()
print("servo zavrsio")
#RFIDLED.value(1)

# Ovaj while se nece puno mijenjati samo treba citati mqtt i mozda displej postavljati
# I to mozda na timer staviti
while 1:
  #MQTTClient.mqtt_conn.check_msg()
    pass
  
  
