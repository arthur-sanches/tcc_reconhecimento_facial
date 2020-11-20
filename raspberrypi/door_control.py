import RPi.GPIO as GPIO
from time import sleep

class Door():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16, GPIO.OUT)

    def open(self):
        GPIO.output(16, True)
        sleep(0.1)
        GPIO.output(16, False)
        sleep(9)
