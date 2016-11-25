from sense_hat import SenseHat

sense = SenseHat()

while True:
    orientation=sense.get_orientation()
    pitch=orientation['pitch']
    roll=orientation['roll']
    yaw=orientation['yaw']
    print("pitch={0}, roll={1}, yaw={2}".format(pitch,roll,yaw))
