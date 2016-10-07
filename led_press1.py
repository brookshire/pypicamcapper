#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
import RPi.GPIO as GPIO
import time

BUTTON = 4
LED1 = 17
LED2 = 18

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED1, GPIO.OUT)
print("PIN %d SET FOR OUTPUT" % LED1)

GPIO.setup(LED2, GPIO.OUT)
print("PIN %d SET FOR OUTPUT" % LED2)

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("PIN %d SET FOR INPUT" % BUTTON)

try:
    while True:
        input_state = GPIO.input(BUTTON)

        if not input_state:
            print("Button pressed")
            i = 0
            while not input_state:
                if i % 2:
                    GPIO.output(17, True)
                    GPIO.output(18, False)
                else:
                    GPIO.output(17, False)
                    GPIO.output(18, True)

                i += 1
                time.sleep(0.2)
                input_state = GPIO.input(4)

            print("Button released")
            GPIO.output(17, False)
            GPIO.output(18, False)

except KeyboardInterrupt:
    print("Shutting down")
    # GPIO.output(17, False)
    # GPIO.output(18, False)
    GPIO.cleanup()
    print("Exiting")
