import random
import socket
import sys
import time
import threading
from queue import Queue
from client.const import *

class Snake():
    def __init__(self, matrix, input_queue):
        self.matrix = matrix
        self.input_queue = input_queue
        self.snake_color = RED
        self.food_color = GREEN
        self.pause_color = BLUE
        self.pausexs = [4, 4, 4, 4, 6, 6, 6, 6] # Draw the pause symbol like ||
        self.pauseys = [8, 9, 10, 11, 8, 9, 10, 11]
        self.reset()
        self.loop()

    def reset(self):
        # Snake
        self.xs = [5, 5, 5, 5]
        self.ys = [6, 5, 4, 3]
        self.length = 4
        self.f = []
        self.f.extend(range(0,2))
        self.f[0] = random.randint(0, 9)
        self.f[1] = random.randint(0, 19)
        self.v = 0
        self.changed = 1 
        self.pause = 0 # 0 for running mode and 1 for pause mode
        self.update_screen()

    def update_screen(self):
        s = [[BLACK]*WIDTH for x in range(HEIGHT)]

        s[self.f[1]][self.f[0]] = self.food_color

        for i in range(self.length):
            s[self.ys[i]][self.xs[i]] = self.snake_color

        # For cycle to print pause figure --> can be a source of error cause I dont know how for cycles work on Python :)
        if self.pause == 1:    
            for i in range(len(self.pausexs)):
                s[self.pauseys[i]][self.pausexs[i]] = self.pause_color

        screen = b''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                screen += bytes(s[i][j])

        self.matrix.sendall(screen)

    def checkCollisionObject(self, x1, y1, x2, y2):
        if x1==x2 and y1==y2:
            return True
        else:
            return False

    def checkCollisionWalls(self):
        if self.xs[0]>=0 and self.xs[0]<10 and self.ys[0]>=0 and self.ys[0]<20:
            return False
        else:
            return True

    def checkSelfCollision(self):
        for i in range(1, self.length):
            if self.checkCollisionObject(self.xs[0], self.ys[0], self.xs[i], self.ys[i]):
                return True
        return False

    def checkEatSnake(self):
        if self.checkCollisionObject(self.xs[0], self.ys[0], self.f[0], self.f[1]):
            self.xs.append(self.f[0])
            self.ys.append(self.f[1])
            self.f[0] = random.randint(0, 9)
            self.f[1] = random.randint(0, 19)
            self.length += 1

    def moveSnake(self):
        xs_old = list(self.xs)
        ys_old = list(self.ys)
        for i in range(1, self.length):
            self.xs[i] = xs_old[i-1]
            self.ys[i] = ys_old[i-1]

        if self.v == 0:
            self.ys[0] += 1
        elif self.v == 1:
            self.xs[0] += 1
        elif self.v == 2:
            self.ys[0] -= 1
        elif self.v == 3:
            self.xs[0] -= 1

    def loop(self):
        while True:
            if not self.input_queue.empty():
                btn = self.input_queue.get()

                if btn == 'Select':
                    break

                if btn == 'Start':
                    if self.pause == 0:
                        self.pause = 1 #pause
                        self.update_screen() 
                        # time.sleep(1/(3 + self.length/4)) unecessary???
                        continue
                    else:
                        self.pause = 0; # not on pause anymore

                if self.pause == 1:
                    continue

                if self.changed == 0:
                    if btn == 'Up' and self.v != 0:
                        self.v = 2
                    elif btn == 'Down' and self.v != 2:
                        self.v = 0
                    elif btn == 'Left' and self.v != 1:
                        self.v = 3
                    elif btn == 'Right' and self.v != 3:
                        self.v = 1
                    self.changed = 1

            self.checkEatSnake()
            self.moveSnake()
            self.changed = 0
            if self.checkCollisionWalls() or self.checkSelfCollision():
                # Add sad face or GG letters
                break

            self.update_screen()
            time.sleep(1/(3 + self.length/4))
