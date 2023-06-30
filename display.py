from ili934xnew import ILI9341, color565
from micropython import const
import os
import time
import glcdfont
import tt14
import tt24
import tt32
import time
import machine
from machine import SPI, Pin

class Display:
    _SCR_WIDTH = 320
    _SCR_HEIGHT = 240
    _SCR_ROT = 3
    _CENTER_Y = int(_SCR_WIDTH/2)
    _CENTER_X = int(_SCR_HEIGHT/2)
    _TFT_CLK_PIN = 18
    _TFT_MOSI_PIN = 19
    _TFT_MISO_PIN = 16
    _TFT_CS_PIN = 17
    _TFT_RST_PIN = 20
    _TFT_DC_PIN = 15
    fonts = [glcdfont,tt14,tt24,tt32]

    def __init__(self):
        self.__initialise()


    def __initialise(self):
        self.spi = SPI(
            0,
            baudrate=62500000,
            miso=Pin(self._TFT_MISO_PIN),
            mosi=Pin(self._TFT_MOSI_PIN),
            sck=Pin(self._TFT_CLK_PIN))

        self.display = ILI9341(
            self.spi,
            cs=Pin(self._TFT_CS_PIN),
            dc=Pin(self._TFT_DC_PIN),
            rst=Pin(self._TFT_RST_PIN),
            w=self._SCR_WIDTH,
            h=self._SCR_HEIGHT,
            r=self._SCR_ROT)
        print(self.spi)
        self.display.erase()
        



    def draw_vline(self,x,y):
        for i in range(y,self._SCR_HEIGHT-y):
            self.display.pixel(x,i+y,color565(255,255,255))

    def draw_hline(self,x,y):
        for i in range(x,self._SCR_WIDTH-x):
            self.display.pixel(x+i,y,color565(255,255,255))

    


    def default_display(self, freeSpaces):
        self.display.erase()
        self.display.set_pos(0,0)
        self.display.set_font(glcdfont)
        self.display.set_color(color565(255,255,255),color565(0,0,0))
        self.display.set_pos(25,70)
        self.display.set_font(tt32)
        printString = 'DOBRODOSLI NA PARKING, TRENUTNO SLOBODNO ' + str(freeSpaces) + ' MJESTA'
        self.display.print(printString)

    def display_welcome(self, freeSpaces):
        self.display.erase()
        self.display.set_font(tt32)
        self.display.set_color(color565(0, 128, 0), color565(0,0,0))
        self.display.set_pos(40,100)
        self.display.print("PRISTUP ODOBREN, DOBRODOSLI")
        self.default_display(freeSpaces)
    
    def display_leave(self, freeSpaces):
        self.display.erase()
        self.display.set_font(tt32)
        self.display.set_color(color565(0, 128, 0), color565(0,0,0))
        self.display.set_pos(40,100)
        self.display.print("DOVIDJENJA POSJETITE NAS OPET")
        self.default_display(freeSpaces)

    def display_error(self, freeSpaces):
        self.display.erase()
        self.display.set_font(tt32)
        self.display.set_color(color565(128, 0, 0), color565(0,0,0))
        self.display.set_pos(40,100)
        self.display.print("PRISTUP ODBIJEN")
        self.default_display(freeSpaces)

    def display_full(self, freeSpaces):
        self.display.erase()
        self.display.set_font(tt32)
        self.display.set_color(color565(128, 0, 0), color565(0,0,0))
        self.display.set_pos(40,100)
        self.display.print("PARKING JE POPUNJEN SACEKAJTE")
        self.default_display(freeSpaces)

    def draw_circle(self,xpos0, ypos0, rad, col=color565(255, 255, 255)):
        x = rad - 1
        y = 0
        dx = 1
        dy = 1
        err = dx - (rad << 1)
        while x >= y:
            self.display.pixel(xpos0 + x, ypos0 + y, col)
            self.display.pixel(xpos0 + y, ypos0 + x, col)
            self.display.pixel(xpos0 - y, ypos0 + x, col)
            self.display.pixel(xpos0 - x, ypos0 + y, col)
            self.display.pixel(xpos0 - x, ypos0 - y, col)
            self.display.pixel(xpos0 - y, ypos0 - x, col)
            self.display.pixel(xpos0 + y, ypos0 - x, col)
            self.display.pixel(xpos0 + x, ypos0 - y, col)
            if err <= 0:
                y += 1
                err += dy
                dy += 2
            if err > 0:
                x -= 1
                dx += 2
                err += dx - (rad << 1)

