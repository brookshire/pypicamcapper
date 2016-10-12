from sense_hat import SenseHat
import datetime
sense = SenseHat()
sense.set_rotation(180)
#sense.show_message("IoT Sensor Pack")
#sense.show_message(str(datetime.datetime.now()))

try:
    while True:
       sense.show_message(str(datetime.datetime.now()))
except KeyboardInterrupt:
    sense.clear()

 
