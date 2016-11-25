from sense_hat import SenseHat
from time import sleep
import random

sense = SenseHat()
while(True):
    r = random.randrange(255)
    g = random.randrange(255)
    b = random.randrange(255)
    sense.show_letter("S",text_colour=[r,g,b])
    sleep(.2)
