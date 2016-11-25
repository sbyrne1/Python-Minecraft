from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()


a=[178,107,66]
b=[73,255,33]
c=[255,93,0]
d=[94,89,204]
e=[8,0,178]
f=[0,0,0]   # e stands for empty/black

image= [
a,a,a,a,f,a,a,a,
a,a,a,a,f,a,a,a,
b,b,b,b,f,b,b,b,
c,c,c,c,f,c,c,c,
d,d,d,d,f,d,d,d,
e,e,e,e,f,e,e,e,
e,e,e,e,f,e,e,e,
f,f,f,f,f,f,f,f
]

sense.set_pixels(image)

sleep(5)

sense.set_rotation(180)

sleep(5)

sense.clear()
