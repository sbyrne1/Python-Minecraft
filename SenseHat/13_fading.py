from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()


while True:
    for r in range(255):
        a=[r,0,0]

        image= [
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a,
        a,a,a,a,a,a,a,a
        ]

        sense.set_pixels(image)
        sleep(.05)
