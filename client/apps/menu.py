import socket
import sys
import time
import threading
from queue import Queue
from client.const import *

class Menu:
    def __init__(self, matrix, input_queue):
        self.matrix = matrix
        self.input_queue = input_queue

        self.screen = [[(0,0,0)] * WIDTH for i in range(HEIGHT)]
        self.app_list = ['tetris', 'snake', 'rainbow','bemvindo']
        self.app_colors = [RED, GREEN, BLUE,WHITE]
        self.app = 0
        self.new_app = 0

        self.draw_menu()
        self.loop()

    def update_screen(self):
        screen = b''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                screen += bytes(self.screen[i][j])
        self.matrix.sendall(screen)

    def draw_menu(self):
        for i, color in enumerate(self.app_colors):
            self.screen[2*i + 2][8] = color
            self.screen[2*i + 2][7] = color

        self.screen[2*self.app + 2][1] = WHITE
        self.update_screen()

    def update_menu(self):
        self.screen[2*self.app + 2][1] = BLACK
        self.screen[2*self.new_app + 2][1] = WHITE
        self.app = self.new_app
        self.update_screen()

    def up_key(self):
        if self.app >= 1:
            self.new_app = self.app - 1
            self.update_menu()

    def down_key(self):
        if self.app < len(self.app_list) - 1:
            self.new_app = self.app + 1
            self.update_menu()

    def a_key(self):
        app = self.app_list[self.app]
        exec('from client.apps.{0} import {1} as App'.format(app, app.capitalize()), globals())
        App(self.matrix, self.input_queue)
        time.sleep(MIN_PERIOD)
        self.draw_menu()

    def loop(self):
        while True:
            if not self.input_queue.empty():
                btn = self.input_queue.get()

                if btn == 'Up':
                    self.up_key()
                elif btn == 'Down':
                    self.down_key()
                elif btn == 'A':
                    self.a_key()
                    self.draw_menu()
            time.sleep(MIN_PERIOD)
