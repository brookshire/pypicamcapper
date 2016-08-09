#
# Copyright (C) 2016, David Brookshire <dave@brookshire.org>
#
# Process which will manage periodically capturing an image from a raspberry pi camera, and
# uploading it to a remote(ish) website.
#
import datetime
import os
import re
import subprocess
import time

import picamera

hwaddr_pat = re.compile('HWaddr [0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:([0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2})')

class PyPiCamCapper():
    cap_path = "/tmp"
    cap_wait = 5 # seconds
    stitch_cleanup = False

    def __init__(self, *args, **kwargs):
        self.cam = picamera.PiCamera()
        # self.fname = self.get_fname
        # super(PyPiCamCapper, self).__init__(args, kwargs)

    @property
    def fname(self):

        cmd = "/sbin/ifconfig eth0"
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             shell=False)
        rc = p.wait()
        line = p.stdout.readline()
        mo = hwaddr_pat.search(line, re.IGNORECASE)
        if not mo:
            ret = "image"
        else:
            ret = mo.group(1).replace(':', '')

        return ret

    def run(self):
        while True:
            fname = self.fname + '-' + datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S") + '.jpg'
            out = os.path.join(self.cap_path, fname)
            print("Capturing camera to " + out)
            self.cam.capture(out)
            time.sleep(self.cap_wait)

if __name__ == '__main__':
    x = PyPiCamCapper()
    x.cap_path = "/var/www/html"
    try:
        x.run()
    except KeyboardInterrupt:
        pass
        # x.stitch()