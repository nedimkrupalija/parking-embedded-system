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


# 27 Wiegand Pin1
# 28 Wiegand Pin2


############## MQTT BROKER TEME  ##################

TEMAPROSTOR = 'projekat/parking'


parkingSize = 5 # Broj parking mjesta
currentUsersList = [] # Primjer

#def motora
servoMotor = Servo(pin=21)

MQTTClient = MQTTClass()
taster = Pin(0, Pin.IN)

#41668, 21966 ID-evi kartica
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


WIEGAND_ZERO = 27  
WIEGAND_ONE = 28   

DisplayObject = Display()
freeSpaces = parkingSize - len(currentUsersList)
DisplayObject.default_display(freeSpaces)
if freeSpaces > 0:
    GREEN_LED.value(1)
    RED_LED.value(0)
else:
    GREEN_LED.value(0)
    RED_LED.value(1)


scanningBool = False


 
def _returnTrue(timer):
    global scanningBool
    scanningBool = False
    

def on_card(card_number, facility_code, cards_read):
    global scanningBool, _returnTrue
    
    if scanningBool == True:
        print(scanningBool, "aa")
        return
    scanningBool = True
    timerMain = Timer(-1)
    timerMain.init(mode=Timer.ONE_SHOT, period=200, callback=_returnTrue)
    
    if (card_number in VALID_CARDS) and (facility_code in VALID_FACILITY_CODES):
        
        publishString = "Korisnik id: " + str(card_number) + " je "
        if(card_number in currentUsersList):
            publishString = publishString + "izasao s parkinga."
            currentUsersList.remove(card_number)
            freeSpaces = parkingSize - len(currentUsersList)
            DisplayObject.display_leave(freeSpaces)
            RED_LED.value(0)
            GREEN_LED.value(1)
        else:
            freeSpaces = parkingSize - len(currentUsersList)
            if (freeSpaces) == 0:
                DisplayObject.display_full(freeSpaces)
                return
            publishString = publishString + "usao na parking."
            currentUsersList.append(card_number)
            freeSpaces = parkingSize - len(currentUsersList)
            if freeSpaces == 0:
                RED_LED.value(1)
                GREEN_LED.value(0)
            DisplayObject.display_welcome(freeSpaces)
            
        publishString = publishString + " Trenutno " + str(len(currentUsersList)) + " vozila."
        MQTTClient.mqtt_conn.publish(TEMAPROSTOR, publishString)
        servoMotor.openRamp()
    else:
        
        freeSpaces = parkingSize - len(currentUsersList)
        DisplayObject.display_error(freeSpaces)
        
Wiegand(WIEGAND_ZERO, WIEGAND_ONE, on_card)



while 1:
    pass
  
  