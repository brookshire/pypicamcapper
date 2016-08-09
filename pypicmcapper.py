#
# Copyright (C) 2016, David Brookshire <dave@brookshire.org>
#
# Process which will manage periodically capturing an image from a raspberry pi camera, and
# uploading it to a remote(ish) website.
#
import datetime
import logging
import os
import re
import subprocess
import sys
import time

import picamera

# Regex to provide a unique'ish identifier for naming image capture files.
hwaddr_pat = re.compile('HWaddr [0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:([0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2})')

# Credit to Hitchhiker's Guide to Python
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

class PyPiCamCapper():
    logger = logging.getLogger(__name__)#.addHandler(NullHandler)
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger_handler.setLevel(logging.DEBUG)
    logger.addHandler(logger_handler)
    logger.setLevel(logging.DEBUG)

    cap_path = "/tmp"
    cap_wait = 5 # seconds
    stitch_cleanup = False

    def __init__(self, *args, **kwargs):
        """
        Initialize the picamera object at the time we create a PyPiCamCapper instance.

        :param args:
        :param kwargs:
        """
        self.cam = picamera.PiCamera()

    @property
    def fname(self):
        """
        Determine what the image files from this pi should be named--for now we're using the last three values of
        the MAC address of eth0, as reported by the ifconfig command.  Not truly unique, but good enough for our
        purposes here.

        :return: Return a string to be used in naming the image capture files base on this specific computer.
        """

        cmd = "/sbin/ifconfig eth0"
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             shell=False)
        rc = p.wait()

        line = p.stdout.readline()
        mo = hwaddr_pat.search(line, re.IGNORECASE)
        if not mo:
            # provide a default value should the ifconfig command above fail to return something useful.
            ret = "image"
        else:
            # use the matching values, but concatenate the hex values, removing the ':' characters.
            ret = mo.group(1).replace(':', '')

        return ret

    def run(self):
        self.logger.info("Starting capture, every %d seconds, to %s, named %s." % (self.cap_wait,
                                                                                   self.cap_path,
                                                                                   self.fname))

        while True:
            cap_name = self.fname + '-' + datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + '.jpg'
            cap_out = os.path.join(self.cap_path, cap_name)
            self.logger.info("Capturing " + cap_out)
            self.cam.capture(cap_out)
            time.sleep(self.cap_wait)

if __name__ == '__main__':
    x = PyPiCamCapper()
    x.cap_path = "/var/www/html"
    try:
        x.run()
    except KeyboardInterrupt:
        x.logger.info("Capture complete.")
        pass
        # x.stitch()