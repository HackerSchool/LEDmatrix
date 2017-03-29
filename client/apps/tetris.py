import random
import sys
import time
import threading
from queue import Queue

from client.const import *

DROP_PERIOD = 0.8

class Piece:
    def __init__(self):
        self.state = random.randint(0, len(self.rotations)-1)
        self.pos  = (4,0)

    def rotate(self):
        self.state = (self.state + 1) % len(self.rotations)

    def inv_rotate(self):
        self.state = (self.state - 1) % len(self.rotations)
        if self.state == -1:
            self.state = len(self.rotations) - 1

    def get_state(self):
        return self.rotations[self.state]

class T(Piece):
    color = (255,0,0)
    rotations =[[(1,0), (0,1), (1,1), (2,1)],
                [(0,0), (0,1), (1,1), (0,2)],
                [(0,0), (1,0), (1,1), (2,0)],
                [(1,1), (0,1), (1,0), (1,2)]]

class L(Piece):
    color = (0,0,255)
    rotations =[[(0,0), (1,0), (1,1), (1,2)],
                [(0,1), (1,1), (2,1), (2,0)],
                [(0,0), (0,1), (0,2), (1,2)],
                [(0,0), (0,1), (1,0), (2,0)]]

class J(Piece):
    color = (0,255,0)
    rotations =[[(0,0), (1,0), (0,1), (0,2)],
                [(0,0), (1,0), (2,0), (2,1)],
                [(1,0), (0,2), (1,1), (1,2)],
                [(0,0), (0,1), (1,1), (2,1)]]

class I(Piece):
    color = (255,255,0)
    rotations =[[(0,0), (0,1), (0,2), (0,3)],
                [(0,0), (1,0), (2,0), (3,0)]]

class S(Piece):
    color = (255,0,255)
    rotations =[[(1,0), (2,0), (0,1), (1,1)],
                [(0,0), (0,1), (1,1), (1,2)]]

class Z(Piece):
    color = (50,100,100)
    rotations =[[(0,0), (1,0), (1,1), (2,1)],
                [(1,0), (0,1), (1,1), (0,2)]]

class O(Piece):
    color = (0,255,255)
    rotations =[[(0,0), (1,0), (0,1), (1,1)]]

PIECE_TYPES = (T, L, J, I, S, Z, O)

class Tetris:
    def __init__(self, matrix, input_queue):
        self.s = matrix
        self.input_queue = input_queue
        self.wait_new = False
        self.clear()
        self.loop()

    def clear(self):
        self.table = [[(0,0,0)] * WIDTH for i in range(HEIGHT)]
        self.score = 0
        self.update_screen()

    def check_collision(self):
        pos_state = self.piece.get_state()
        for i in range(4):
            if self.piece.pos[0] + pos_state[i][0] > 9 :
                return True
            if self.piece.pos[1] + pos_state[i][1] > 19 :
                return True
            if self.table[self.piece.pos[1] + pos_state[i][1]][self.piece.pos[0] + pos_state[i][0]] != (0,0,0):
                return True
        return False

    def new_piece(self):
        self.piece = random.choice(PIECE_TYPES)()
        if self.check_collision():
            self.game_over()
            return

        self.draw_piece()
        self.update_screen()

    def check_lines(self):
        for i in range(HEIGHT):
            total = 0
            for j in range(WIDTH):
                if self.table[i][j] == (0,0,0):
                    total+=1
                    break
            if total == 0:
                self.score += 1
                old_table = list(self.table)
                self.table[0] = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
                for w in range(0, i):
                    self.table[w+1] = old_table[w]

    def next_tick(self):
        self.clean_piece()
        self.piece.pos = (self.piece.pos[0],self.piece.pos[1]+1)
        if self.check_collision():
            # colision let draw piece in before position
            self.piece.pos = (self.piece.pos[0],self.piece.pos[1]-1)
            self.draw_piece()
            self.check_lines()
            self.new_piece()
        else:
            self.draw_piece()
            self.update_screen()

    def draw_piece(self):
        pos_state = self.piece.get_state()
        for i in range(4):
            x  = self.piece.pos[0] + pos_state[i][0]
            y =  self.piece.pos[1] + pos_state[i][1]
            self.table[y][x] = self.piece.color

    def clean_piece(self):
        pos_state = self.piece.get_state()
        for i in range(4):
            x  = self.piece.pos[0] + pos_state[i][0]
            y =  self.piece.pos[1] + pos_state[i][1]
            self.table[y][x] = (0,0,0)

    def update_screen(self):
        screen = b''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                screen += bytes(self.table[i][j])

        self.s.sendall(screen)

    def left_key(self):
        if self.piece.pos[0]-1 >= 0:
            self.clean_piece()
            self.piece.pos = (self.piece.pos[0]-1,self.piece.pos[1])
            if(self.check_collision()): # ilegal movement
                self.piece.pos = (self.piece.pos[0]+1,self.piece.pos[1])
                self.draw_piece()
            else:
                self.draw_piece()
                self.update_screen()

    def right_key(self):
        if self.piece.pos[0]+1 < 20 :
            self.clean_piece()
            self.piece.pos = (self.piece.pos[0]+1,self.piece.pos[1])
            if(self.check_collision()): # ilegal movement
                self.piece.pos = (self.piece.pos[0]-1,self.piece.pos[1])
                self.draw_piece()
            else:
                self.draw_piece()
                self.update_screen()

    def down_key(self):
        self.clean_piece()
        self.piece.pos = (self.piece.pos[0],self.piece.pos[1]+1)
        if(self.check_collision()):
            # colision let draw piece in before position
            self.piece.pos = (self.piece.pos[0],self.piece.pos[1]-1)
            self.draw_piece()
        else:
            self.draw_piece()
            self.update_screen()

    def up_key(self):
        self.clean_piece()
        self.piece.rotate()
        if(self.check_collision()): # ilegal movement
            self.piece.inv_rotate()
            self.draw_piece()
        else:
            self.draw_piece()
            self.update_screen()

    def start_key(self):
        saved = []
        for i in range(WIDTH):
            saved.append(self.table[10][i])
            self.table[10][i] = (0xFF, 0x8A, 0x00)
        self.update_screen()

        while True:
            if not self.input_queue.empty():
                btn = self.input_queue.get()
                if btn == 'Start':
                    break
            time.sleep(0.1)

        for i in range(WIDTH):
            self.table[10][i] = saved[i]
        self.update_screen()


    def a_key(self):
        self.clean_piece()
        while not self.check_collision():
            self.piece.pos = (self.piece.pos[0],self.piece.pos[1]+1)
        self.piece.pos = (self.piece.pos[0],self.piece.pos[1]-1)
        self.draw_piece()
        self.update_screen()

    def game_over(self):
        for i in range(20):
            for j in range(10):
                self.table[i][j] = (0, 0, 0)

        self.table[3][3] = (255, 0, 0)
        self.table[4][3] = (255, 0, 0)
        self.table[5][3] = (255, 0, 0)
        self.table[6][3] = (255, 0, 0)
        self.table[3][6] = (255, 0, 0)
        self.table[4][6] = (255, 0, 0)
        self.table[5][6] = (255, 0, 0)
        self.table[6][6] = (255, 0, 0)

        self.table[9][3] = (255, 0, 0)
        self.table[9][4] = (255, 0, 0)
        self.table[9][5] = (255, 0, 0)
        self.table[9][6] = (255, 0, 0)
        self.table[10][2] = (255, 0, 0)
        self.table[10][7] = (255, 0, 0)
        self.table[11][1] = (255, 0, 0)
        self.table[11][8] = (255, 0, 0)
        self.table[12][0] = (255, 0, 0)
        self.table[12][9] = (255, 0, 0)


        inv_mask = '{:010b}'.format(self.score)
        for i, bit in enumerate(inv_mask):
            if bit == '1':
                self.table[19][i] = (0x00, 0xFF, 0x00)
        self.update_screen()
        self.wait_new = True

    def wait_end_game(self):
        quit = False

        while True:
            if not self.input_queue.empty():
                btn = self.input_queue.get()
                if btn == 'Start':
                    break
                if btn == 'Select':
                    quit = True
                    break
            time.sleep(0.1)
        self.wait_new = False
        self.clear()

        return quit


    def loop(self):
        self.new_piece()
        now = time.perf_counter
        last_drop = now()

        while True:
            if self.wait_new:
                if self.wait_end_game():
                    break

            if not self.input_queue.empty():
                btn = self.input_queue.get()

                if btn == 'Up':
                    self.up_key()
                elif btn == 'Down':
                    self.down_key()
                elif btn == 'Left':
                    self.left_key()
                elif btn == 'Right':
                    self.right_key()
                elif btn == 'A':
                    self.a_key()
                elif btn == 'Start':
                    self.start_key()
                elif btn == 'Select':
                    self.clear()
                    break

            else:
                if now() - last_drop < DROP_PERIOD:
                    time.sleep(30e-3)
                    continue

            time.sleep(MIN_PERIOD)
            self.next_tick()
            last_drop = now()
