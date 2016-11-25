# spiral
from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()
sense.clear()

while True:
    minx=0
    maxx=7
    miny=0
    maxy=7

    r=randint(0,255)
    g=randint(0,255)
    b=255
    step=3

    sense.low_light = True

    j=miny
    for a in range(4):
        for i in range(minx,maxx+1):
            sense.set_pixel(i,j,[r,g,b])
            b-=step
            sleep(0.2)        
        miny+=1
        for j in range(miny,maxy+1):
            sense.set_pixel(i,j,[r,g,b])
            b-=step
            sleep(0.2)        
        maxx-=1
        for i in range(maxx,minx-1,-1):
            sense.set_pixel(i,j,[r,g,b])
            b-=step
            sleep(0.2)
        maxy-=1
        for j in range(maxy,miny-1,-1):
            sense.set_pixel(i,j,[r,g,b])
            b-=step
            sleep(0.2)
        minx+=1
       
