from sense_hat import SenseHat

sense = SenseHat()

sense.show_letter("B")

while True:
    accel=sense.get_accelerometer_raw()
    x=accel['x']
    y=accel['y']
    z=accel['z']

    x=round(x,0)
    y=round(y,0)

    if x==-1:
        sense.set_rotation(90)
    elif y==1:
        sense.set_rotation(0)
    elif y==-1:
        sense.set_rotation(180)
    else:
        sense.set_rotation(270)
