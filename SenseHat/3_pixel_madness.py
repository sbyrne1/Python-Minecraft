from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()

for i in range(8):
    for j in range(8):
        r=randint(0,255)
        g=randint(0,255)
        b=randint(0,255)
        sense.set_pixel(i,j,[r,g,b])
        

