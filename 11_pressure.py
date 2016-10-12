from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

temp = sense.get_temperature_from_pressure()
temp = round(temp, 1)
print(temp)
