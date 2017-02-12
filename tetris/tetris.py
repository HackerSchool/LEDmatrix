import random
import pygame
from pygame.locals import *
import socket
import sys
import time

class Piece:

    def __init__(self):
        self.state = random.randint(0, len(self.rotations)-1)
        self.pos  = (4,0)
    def rotate(self):
        self.state = (self.state + 1) % len(self.rotations)

    def get_state(self):
        return self.rotations[self.state]

    @classmethod
    def get_color(cls):
        return cls.color


class T(Piece):
    color = (255,0,0)
    rotations =[[(0,1), (1,0), (1,1), (1,2)],
                [(0,0), (1,0), (1,1), (2,0)],
                [(0,0), (0,1), (1,1), (0,2)],
                [(0,1), (1,1), (1,2), (1,0)]]

class L(Piece):
    color = (255,0,0)
    rotations =[[(0,0), (0,1), (1,1), (2,1)],
                [(1,0), (1,1), (1,2), (0,2)],
                [(0,0), (1,0), (2,0), (2,1)],
                [(0,0), (0,1), (0,2), (1,0)]]

class J(Piece):
    color = (255,0,0)
    rotations =[[(0,0), (0,1), (1,0), (2,0)],
                [(0,0), (0,1), (0,2), (1,2)],
                [(0,1), (0,2), (1,1), (1,2)],
                [(0,0), (1,0), (1,1), (1,2)]]

class I(Piece):
    color = (255,0,0)
    rotations =[[(0,0), (1,0), (2,0), (3,0)],
                [(0,0), (0,1), (0,2), (0,3)]]

class S(Piece):
    color = (255,0,0)
    rotations =[[(0,1), (0,2), (1,0), (1,1)],
                [(0,0), (1,0), (1,1), (2,1)]]

class Z(Piece):
    color = (255,0,0)
    rotations =[[(0,0), (0,1), (1,1), (1,2)],
                [(0,1), (1,0), (1,1), (2,0)]]

class O(Piece):
    color = (255,0,0)
    rotations =[[(0,0), (1,0), (0,1), (1,1)]]

piece_types = (T, L, J, I, S, Z, O)

class Tetris:

    def __init__(self, HOST, PORT):
        self.table = [[(0,0,0)]*10 for i in range(20)]
        print(self.table)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        self.new_piece()
        self.i = 0

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
        self.piece = random.choice(piece_types)()
        if(self.check_collision()):
            print("game over")
            sys.exit()
        self.draw_piece()
        self.update_screen()

    def next_tick(self):
        self.rigth_key()
        self.clean_piece()
        self.piece.pos = (self.piece.pos[0],self.piece.pos[1]+1)
        print(self.piece.pos)
        if(self.check_collision()):
            # colision let draw piece in before position
            self.piece.pos = (self.piece.pos[0],self.piece.pos[1]-1)
            self.draw_piece()
            # check complete line
            self.new_piece()
        else:
            self.draw_piece()
            self.update_screen()

    def draw_piece(self):
        pos_state = self.piece.get_state()
        for i in range(4):
            x  = self.piece.pos[0] + pos_state[i][0]
            y =  self.piece.pos[1] + pos_state[i][1]
            self.table[y][x] = self.piece.get_color()

    def clean_piece(self):
        pos_state = self.piece.get_state()
        for i in range(4):
            x  = self.piece.pos[0] + pos_state[i][0]
            y =  self.piece.pos[1] + pos_state[i][1]
            self.table[y][x] = (0,0,0)

    def update_screen(self):
        mensage = ""
        for j in range(20):
            for i in range(10):
                mensage = mensage + str(self.table[j][i][0]) + "|"
                mensage = mensage + str(self.table[j][i][1]) + "|"
                mensage = mensage + str(self.table[j][i][2]) + "|"
        self.s.sendall(mensage.encode('UTF-8'))
        time.sleep(1)
        # before must be call by pygame tick
        self.next_tick()

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

    def rigth_key(self):
        if self.piece.pos[0]+1 < 20 :
            self.clean_piece()
            self.piece.pos = (self.piece.pos[0]+1,self.piece.pos[1])
            if(self.check_collision()): # ilegal movement
                self.piece.pos = (self.piece.pos[0]-1,self.piece.pos[1])
                self.draw_piece()
            else:
                self.draw_piece()
                #self.update_screen()

    def down_key(self):
        # increment y until colision
        pass

    def up_key(self):
        # rotate and check_collision
        pass

def main():

    HOST = '127.0.0.1'  # The remote host
    PORT = 9500         # The same port as used by the server

    game = Tetris(HOST, PORT)
    i = input("")
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
