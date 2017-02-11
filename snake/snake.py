import random
import pygame
from pygame.locals import *
import socket
import sys


def update_screen(s,xs,ys,lenght,f):
    snake_color = {'R': 255 , 'G': 0, 'B': 0}
    food_color = {'R': 0 , 'G': 255, 'B': 0}
    w = 10
    h = 20
    r = [[0 for x in range(w)] for y in range(h)]
    g = [[0 for x in range(w)] for y in range(h)]
    b = [[0 for x in range(w)] for y in range(h)]
    for i in range(h):
        for j in range(w):
            r[i][j]=0
            g[i][j]=0
            b[i][j]=0

    r[f[1]][f[0]] = food_color['R']
    g[f[1]][f[0]] = food_color['G']
    b[f[1]][f[0]] = food_color['B']

    for i in range(lenght):
        r[ys[i]][xs[i]] = snake_color['R']
        g[ys[i]][xs[i]] = snake_color['G']
        b[ys[i]][xs[i]] = snake_color['B']


    mensage = ""
    for j in range(h):
        for i in range(w):
            mensage = mensage + str(r[j][i]) + "|"
            mensage = mensage + str(g[j][i]) + "|"
            mensage = mensage + str(b[j][i]) + "|"

    s.sendall(mensage.encode('UTF-8'))

def checkCollisionObject(x1, y1, x2, y2):
    if x1==x2 and y1==y2:
        return True
    else:
        return False

def checkCollisionWalls(xs, ys):
    if xs[0]>=0 and xs[0]<10 and ys[0]>=0 and ys[0]<20:
        return False
    else:
        return True

def checkSelfCollision(ys, xs, leng):
    for i in range(1, leng-1):
        if(checkCollisionObject(xs[0], ys[0], xs[i], ys[i])):
            return True
    return False

def checkEatSnake(xs, ys, leng, f):
    if(checkCollisionObject(xs[0], ys[0], f[0], f[1])):
        xs.append(f[0])
        ys.append(f[1])
        f[0] = random.randint(0, 9)
        f[1] = random.randint(0, 19)
        return leng + 1
    else:
        return leng

def moveSnake(leng, xs, ys, v):
    xs_old = list(xs)
    ys_old = list(ys)
    for i in range(1, leng):
        xs[i]=xs_old[i-1]
        ys[i]=ys_old[i-1]

    if(v == 0):
        ys[0] = ys[0] + 1
    elif(v == 1):
        xs[0] = xs[0] + 1
    elif(v == 2):
        ys[0] = ys[0] - 1
    elif(v == 3):
        xs[0] = xs[0] - 1

    for i in range(leng):
        print("X="+str(xs[i])+"; Y="+str(ys[i]))


#def vec_conv
def main():


    HOST = '127.0.0.1'  # The remote host
    PORT = 9500         # The same port as used by the server


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Connection with matrix

        # Snake
        xs = [5, 5, 5,5]
        ys = [6, 5, 4,3]
        leng = 4
        f = []
        f.extend(range(0,2))
        f[0] = random.randint(0, 9)
        f[1] = random.randint(0, 19)
        v = 0
        game = True
        changed = 1
        update_screen(s, xs, ys, leng, f)
        pygame.init()
        screen=pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Snake')
        clock = pygame.time.Clock()
        while game:
            clock.tick(3 + leng/4)
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit(0)
                elif e.type == KEYDOWN and changed == 0:
                    if   e.key == K_UP    and v != 0:
                        v = 2
                    elif e.key == K_DOWN  and v != 2:
                        v = 0
                    elif e.key == K_LEFT  and v != 1:
                        v = 3
                    elif e.key == K_RIGHT and v != 3:
                        v = 1
                    changed = 1
            leng = checkEatSnake(xs, ys, leng, f)
            moveSnake(leng, xs, ys, v)
            changed = 0
            if(checkCollisionWalls(xs, ys) or checkSelfCollision(ys, xs, leng)):
                break
            update_screen(s, xs, ys, leng, f)
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
