from sense_hat import SenseHat
from time import sleep
from math import trunc

def con_to_color( blah ):
    c = trunc ((255/360) * blah)
    return c
    
sense = SenseHat()
while True:
    #orientation_rad = sense.get_orientation_radians()
    #print("radians -- p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))
    orientation_deg = sense.get_orientation_degrees()
    #print("degrees -- p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_deg))

    r = con_to_color(orientation_deg['pitch'])
    g = con_to_color(orientation_deg['roll'])
    b = con_to_color(orientation_deg['yaw'])
    sense.show_letter("S",text_colour=[r,g,b])
    sleep(0.1)
    
