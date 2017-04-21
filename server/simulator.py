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
VERTICAL = True  # False rotates left to horizontal. VISUAL ONLY, COORDINATES DON'T CHANGE!

def network_thread(queue):
    s = socket.socket()
    s.bind(('localhost', PORT))
    s.listen(3)

    while True:
        conn, addr = s.accept()
        while True:
            leds = conn.recv(NUM_BYTES)

            if len(leds) != NUM_BYTES:
                conn.close()
                break

            q.put(leds)


pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE if VERTICAL else HEIGHT * SCALE,
                                  HEIGHT * SCALE if VERTICAL else WIDTH * SCALE))
pygame.display.set_caption("LED Matrix simulation")

clock = pygame.time.Clock()

q = Queue()
thread = threading.Thread(target=network_thread, args=(q,))
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
                             ((p % WIDTH) * SCALE if VERTICAL else (p // WIDTH) * SCALE,  # pixel x (width) location
                              (p // WIDTH) * SCALE if VERTICAL else (WIDTH - (p % WIDTH) - 1) * SCALE,  # pixel y (height) location
                              SCALE,            # pixel height
                              SCALE))           # pixel width

        pygame.display.flip()  # update the window
