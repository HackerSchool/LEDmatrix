from serial import Serial
from serial.tools.list_ports import comports
import time
import sys

BAUD = 9600
PATH = '/dev/ttyUSB1'
CHALL = b"Hi. Who are you?"
RESP = b"Hi. I'm HES."

class Hesv1:
    def __init__(self, input_queue):
        self.input_queue = input_queue
        self.bindings = ['Select', 'Start', 'Up', 'Down', 'Left', 'Right', 'A', 'B']
        while True:
            try:
                self.hesv1 = self.find_hesv1()
                break
            except:
                pass
            finally:
                time.sleep(0.1)

        if not self.hesv1:
            raise Exception('HESv1 Error: HESv1 device not found.')

        self.loop()

    def find_hesv1(self):
        dev = Serial(PATH, BAUD)
        time.sleep(2)

        dev.write(CHALL)
        reply = dev.read(len(RESP))
        if reply == RESP:
            # HESv1 always sends one empty message on connection.
            # It's weird, so we absorb that first read.
            dev.read()
            dev.timeout = None
            return dev

    def read(self):
        d = self.hesv1.readline().rstrip().decode()
        if d:
            return d[0], self.bindings[int(d[1])]

    def loop(self):
        while True:
            act, btn = self.read()
            if act == 'R':
                continue
            self.input_queue.put(btn)
