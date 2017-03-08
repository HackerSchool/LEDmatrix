import sys
import os
import serial
from serial.tools.list_ports import comports
import time
import socket
from const import *

# TODO
def find_matrix():
    for portinfo in comports():
        dev = serial.Serial(portinfo.device, BAUD, timeout=4)
        print(dev)
        time.sleep(2)

        print(dev.write(CHALL))
        reply = dev.read(len(REPLY))
        print(reply)
        if reply == REPLY:
            dev.timeout = None
            return dev

    print('Error: matrix not found.', file=sys.stderr)

def xy_convert_vertical(x, y):
    if y % 2 != 0:
        return (y*10 + x)
    else:
        return (y*10 + 9 - x)

def main():
    #matrix = find_matrix()
    matrix = serial.Serial(PATH, BAUD)
    time.sleep(5)

    try:
        os.unlink(SOCK_PATH)
    except:
        pass

    s = socket.socket(socket.AF_UNIX)
    s.bind(SOCK_PATH)
    s.listen(0)
    leds = bytearray(NUM_BYTES)
    while True:
        last = time.perf_counter()
        conn, addr = s.accept()

        while True:
            msg = conn.recv(NUM_BYTES)

            if len(msg) < NUM_BYTES:
                conn.close()
                break

            # can't risk corrupting the matrix by writing too fast
            diff = time.perf_counter() - last
            if diff >= MIN_PERIOD:
                for i in range(NUM_LEDS):
                    line = int(i / 10)
                    column = int(i % 10)
                    matrix_index = xy_convert_vertical(column, line)
                    leds[matrix_index*3] = msg[i*3]
                    leds[matrix_index*3+1] = msg[i*3+1]
                    leds[matrix_index*3+2] = msg[i*3+2]

                matrix.write(leds)
                last = time.perf_counter()

    matrix.close()

if __name__ == '__main__':
    main()
