import sys
import os
import serial
import time
import socket
from const import *

def xy_convert_vertical(x, y):
    if y % 2 != 0:
        return (y*10 + x)
    else:
        return (y*10 + 9 - x)

def main():
    matrix = serial.Serial(PATH, BAUD)
    time.sleep(5)

    try:
        os.unlink(SOCK_PATH)
    except:
        pass

    s = socket.socket(socket.AF_UNIX)
    s.bind(SOCK_PATH)
    s.listen()
    leds = bytearray(NUM_BYTES)
    while True:
        last = time.perf_counter()
        conn, addr = s.accept()

        while True:
            msg = conn.recv(NUM_BYTES)

            if len(msg) < NUM_BYTES:
                print('[+] client is dumb; closed connection.')
                conn.close()
                break

            # can't risk corrupting the matrix, last ditch effort
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
            else:
                print(f'[{time.time()}] dropped frame, diff = {diff} < {MIN_PERIOD}')

    matrix.close()

if __name__ == '__main__':
    main()
