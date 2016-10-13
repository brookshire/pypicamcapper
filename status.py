from sense_hat import SenseHat
import time
import signal
import sys

sense = SenseHat()
sense.set_rotation(180)
# sense.show_message("IoT Sensor Pack")
# sense.show_message(str(datetime.datetime.now()))

def signal_handler(signal, frame):
    print("Shutting down.")
    sense.clear()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

sense.clear()

try:
    while True:
        t = sense.get_temperature()
        p = sense.get_pressure()
        h = sense.get_humidity()

        t = round(t, 1)
        p = round(p, 1)
        h = round(h, 1)

        print("T: %d    P: %d     H: %d" % (t, p, h))

        sense.show_message("T: %d P: %d H: %d" % (t, p, h))
        time.sleep(5)

except KeyboardInterrupt:
    print("Breaking out.")
    sense.clear()
