from sense_hat import SenseHat
from math import trunc

sense = SenseHat()
humidity = sense.get_humidity()
print("Humidity: %s %%rH" % humidity)

pressure = sense.get_pressure()
print("Pressure: %s Millibars" % pressure)
print(sense.pressure)

print(trunc((sense.pressure % 1) * 1000))

# potential uses
# time values
# buffer scrubbing
