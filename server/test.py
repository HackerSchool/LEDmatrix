import serial
import socket
import time
from const import *

BLACK = (0, 0, 0)
RED = (0xff, 0, 0)

def main():
    #matrix = serial.Serial(PATH, BAUD)
    matrix = socket.socket(socket.AF_UNIX)
    matrix.connect(SOCK_PATH)

    time.sleep(5)
    leds = [[BLACK]*WIDTH for _ in range(HEIGHT)]

    while True:
        for x in range(HEIGHT):
            for y in range(WIDTH):
                b = b''
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (i, j) == (x, y):
                            b += bytes(RED)
                        else:
                            b += bytes(BLACK)
                matrix.sendall(b)
                time.sleep(0.1)


if __name__ == '__main__':
    main()
