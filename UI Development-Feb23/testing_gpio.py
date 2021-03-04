import sys
from gpiozero import LED
from time import sleep

led1 = LED(3)

while True:
    led1.on()
    sleep(1)
    led1.off()
    sleep(1)



            