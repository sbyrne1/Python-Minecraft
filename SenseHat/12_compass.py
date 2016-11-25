from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(True, False, False)
north = sense.get_compass()
print("North: %s" % north)
