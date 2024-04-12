
import sys
import RPi.GPIO as GPIO
import time

display_list = [13,6,16,20,21,19,26] # define GPIO ports to use

arrSeg = [[1,1,1,1,1,1,0],\
            [0,1,1,0,0,0,0],\
            [1,1,0,1,1,0,1],\
            [1,1,1,1,0,0,1],\
            [0,1,1,0,0,1,1],\
            [1,0,1,1,0,1,1],\
            [1,0,1,1,1,1,1],\
            [1,1,1,0,0,0,0],\
            [1,1,1,1,1,1,1],\
            [1,1,1,1,0,1,1]]

class Display:
    
    def numero(self, resultado):
            # Use BCM GPIO references instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Set all pins as output
        GPIO.setwarnings(False)
        for pin in display_list:

            GPIO.setup(pin,GPIO.OUT) # setting pins
            GPIO.setup(6,GPIO.OUT) # setting dot pin

        # DIGIT map as array of array

        GPIO.output(6,0) # DOT pi
        
        numDisplay = resultado

        # Display number in argument
        if numDisplay >= 10:
         GPIO.cleanup()

        else:
         GPIO.output(display_list, arrSeg[numDisplay])
         print("Resultado é: ", numDisplay)
         



    """
        numDisplay = 0
        time.sleep(1)
        numDisplay = 1
        time.sleep(1)
        numDisplay = 2
        time.sleep(1)
        numDisplay = 3
        time.sleep(1)
        numDisplay = 4
        time.sleep(1)
        numDisplay = 5
        time.sleep(1)
        numDisplay = 6
        time.sleep(1)
        numDisplay = 7
        time.sleep(1)
        numDisplay = 8
        time.sleep(1)
        numDisplay = 9
        time.sleep(1)
        numDisplay = 9
    """
