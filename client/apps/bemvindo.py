import socket
import time
from client.const import *
from client.apps.image_display import ImageDisplay
from queue import Queue
"""
Bem Vindo
"""

class Bemvindo:
    def __init__(self, matrix, input_queue):
        self.matrix = matrix
        self.input_queue = input_queue
        self.loop()

    def loop(self):
        ImageDisplay(self.matrix, Queue()).print_image("gifs/ist.gif", (0,0,0), 0, True)
