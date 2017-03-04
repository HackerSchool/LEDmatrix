"""
Simulate the real LED matrix in pygame using the same the API (the socket).

Useful for quick devlopment and testing of new apps without physical
access to the actual LED matrix.
"""

import sys, os
import pygame
import socket
import threading
from multiprocessing import Queue
from const import *

SCALE = 32  # Scaling factor so it doesn't actually take only 20x10 pixels on the screen
FPS = 30

def network_thread(SOCK_PATH, queue):
    try:
        os.unlink(SOCK_PATH)
    except:
        pass

    s = socket.socket(socket.AF_UNIX)
    s.bind(SOCK_PATH)
    s.listen()

    while True:
        conn, addr = s.accept()
        while True:
            leds = conn.recv(NUM_BYTES, socket.MSG_WAITALL)

            if len(leds) != NUM_BYTES:
                conn.close()
                break

            q.put(leds)


pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE,
                                  HEIGHT * SCALE))
pygame.display.set_caption("LED Matrix simulation")

clock = pygame.time.Clock()

q = Queue()
thread = threading.Thread(target=network_thread, args=(SOCK_PATH, q))
thread.daemon = True  # if the main thread exits the program won't keep running
thread.start()

while True:
    clock.tick(1/MIN_PERIOD)

    for event in pygame.event.get():  # Necessary for the window close button to work
        if event.type == pygame.QUIT:
            sys.exit()

    if not q.empty():
        leds = q.get()

        for p in range(NUM_LEDS):
            r = p*3
            pygame.draw.rect(screen,
                             (leds[r], leds[r+1], leds[r+2]),  # pixel colors
                             ((p % 10) * SCALE,   # pixel x location
                              (p // 10) * SCALE,  # pixel y location
                              SCALE,            # pixel height
                              SCALE))           # pixel width

        pygame.display.flip()  # update the window
