#
#  Copyright (C) 2016 David Brookshire <dave@brookshire.org>
#
from sense_hat import SenseHat
from time import sleep

from random import randint

min_color_value = 0
max_color_value = 255
delay = 0
increment = 1


def build_display(color):
    i = 0
    ret = []
    while i < 64:
        ret.append(color)
        i += 1
    return ret


sense = SenseHat()

try:
    x = min_color_value + 1
    count_up = True

    while True:
        # print(x)
        if x >= max_color_value:
            # print("Count down")
            count_up = False
        elif x <= min_color_value:
            # print("Count up")
            count_up = True

        if count_up:
            x += increment
        else:
            x -= increment

        sense.set_pixels(build_display([0, x, 0]))
        sleep(delay)


except KeyboardInterrupt:
    sense.clear()
