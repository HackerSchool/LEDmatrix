import socket
import time
from client.const import *

"""
Rainbows!
"""

class Rainbow:
    def __init__(self, matrix, input_queue):
        self.matrix = matrix
        self.input_queue = input_queue
        self.loop()

    def send_color(self, color):
        self.matrix.sendall(color * NUM_LEDS)

        if not self.input_queue.empty():
            btn = self.input_queue.get()
            if btn == 'Select':
                return False
        time.sleep(MIN_PERIOD)
        return True


    def loop(self):
        # `p` is the variable color channel, all the other are fixed,
        # in order to make a 'rainbow' effect. The order of the
        # fixed and variable color channels are easily verified
        # in a color wheel. In RGB order.
        rainbow = [['255 : 0    : {p}' , '{p}  : 0    : 255' ]
                  ,['0   : {p}  : 255' , '0    : 255  : {p}' ]
                  ,['{p} : 255  : 0'   , '255  : {p}  : 0'   ]]

        while True:
            for seg in rainbow:
                # First part of the color segment, `p` increases.
                for p in range(0, 0xff, 2):
                    # format the variable color channel `p` into the string
                    # and turn it into an array of int [R, G, B]
                    color = [int(x) for x in seg[0].format(p=p).split(':')]
                    if not self.send_color(bytes(color)):
                        return

                # In the second part of the color segment,
                # p goes from 0xff to 0 instead.
                for p in reversed(range(0, 0xff, 2)):
                    color = [int(x) for x in seg[1].format(p=p).split(':')]
                    if not self.send_color(bytes(color)):
                        return
