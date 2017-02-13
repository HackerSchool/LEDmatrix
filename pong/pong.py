import random
import pygame
from pygame.locals import *
import socket
import sys
import time
import math

Y_DIRECTIONS = [-1, 1]
X_DIRECTIONS = [-1, 0, 1]

class Raquete:

    def __init__(self, pos):
        self.pos = pos
        self.leng = 3
    def get_pos(self):
        l = [self.pos]
        for i in range(1,(self.leng - 1) // 2 + 1):
            l.append((self.pos[0],self.pos[1]+i))
            l.append((self.pos[0],self.pos[1]-i))
        p  = sorted(l, key= lambda x: x[1])
        return p

    def right_move(self):
        pass

    def left_move(self):
        pass

class Ball:

    def __init__(self):
        self.pos = (9,5)
        self.d = (random.choice(Y_DIRECTIONS),random.choice(X_DIRECTIONS))

    def get_pos(self):
        return [self.pos[0],self.pos[1]]

    def move_ball(self):
        self.pos = (self.pos[0]+self.d[0], self.pos[1]+self.d[1])

    def demove_ball(self):
        self.pos = (self.pos[0]+self.d[0], self.pos[1]+self.d[1])

    def get_d(self):
        return self.d

    def tuggle_direction(self, factor):
        self.d = (self.d[0] * factor[0], self.d[1] * factor[1])
    def change_direction(self):
        pass

class Pong:

    def __init__(self):
        HOST = '127.0.0.1'  # The remote host
        PORT = 9500
        self.player1 = Raquete((19,4))
        self.player2 = Raquete((0,4))
        self.player1_score = 0
        self.player2_score = 0
        self.table = [[(0,0,0)]*10 for i in range(20)]
        self.ball = Ball()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def new_ball(self):
        self.ball = Ball()

    def check_collision(self):
        ball_pos = self.ball.get_pos()
        if(ball_pos[1] < 0 or ball_pos[1] > 9): #ball collides with a wall
            return -1, -1
        elif(ball_pos[0] == 19):
            player1_pos = self.player1.get_pos()
            for i in range(len(player1_pos)):
                if ball_pos[1] == player1_pos[i][1]:
                    #return 0, i #bounces on player 1 raquete
                    return 0
                else:
                #    return 2, -1 #player 2 scores
                   return 2
        elif(ball_pos[0] == 0):
            player2_pos = self.player2.get_pos()
            for i in range(len(player2_pos)):
                if ball_pos[1] == player2_pos[i][1]:
                    #return 0, i #bounces on player 2 raquete
                    return 0, i
                else:
                    #return 1, -1 #player 1 scores
                    return 1 #player 1 scores

    def new_tick(self):
        self.ball.move_ball()

        a = self.check_collision()
        b = 0
        if a == -1: #wall
            self.ball.demove_ball()
            self.ball.tuggle_direction((1,-1))
            self.ball.move_ball()

        elif b == -1: #score
            if a == 1:
                self.player1_score += 1
            elif a == 2:
                self.player2_score += 1
            self.ball.new_ball()

        elif a == 0:
            d = self.ball.get_d()
            if b == 0 :
                if d[1] > 0 :
                    self.ball.tuggle_direction((-1,-1))
                if d[1] <= 0 :
                    self.ball.tuggle_direction((-1,1))
            if b == 1:
                self.ball.tuggle_direction((-1,1))

            if b ==  2:
                if d[1] >= 0 :
                    self.ball.tuggle_direction((-1,1))
                if d[1] < 0 :
                    self.ball.tuggle_direction((-1,-1))
        self.draw()
        self.update_screen()

    def draw(self):

        p1 = self.player1.get_pos()
        p2 = self.player2.get_pos()
        b  = self.ball.get_pos()
        print(b)
        for i in range(len(p1)):
            x = p1[i][1]
            y = p1[i][0]
            self.table[y][x] = (255,0,0)
            x = p2[i][1]
            y = p2[i][0]
            self.table[y][x] = (255,0,0)
        x = b[1]
        y = b[0]
        self.table[y][x] = (0,255,0)

    def update_screen(self):
        message = ""
        for j in range(20):
            for i in range(10):
                message = message + str(self.table[j][i][0]) + "|"
                message = message + str(self.table[j][i][1]) + "|"
                message = message + str(self.table[j][i][2]) + "|"
        self.s.sendall(message.encode('UTF-8'))




def main():


    game = Pong()

    while True :
        time.sleep(1)
        game.new_tick()

if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
