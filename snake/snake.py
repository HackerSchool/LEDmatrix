import random
import pygame

def printObjects:
    return True

def checkCollisionObject(x1, y1, x2, y2):
    if x1==x2 and y1==y1:
        return True
    else:
        return False

def checkCollisionWalls(xs, ys):
    if xs[0]>=0 and xs[0]<10 and ys[0]>=0 and ys[0]<20:
        return False
    else:
        return True

def checkSelfCollision(ys, xs, leng):
    for i in range(1, leng):
        if(checkCollisionObject(x[0], y[0], xs[i], ys[i])):
            return True
    return False

def checkEatSnake(xs, ys, leng, f):
    if(checkCollisionObject(xs[0], ys[0], xf, yf)):
        return leng + 1
        f = (random.randint(0, 9), random.randint(0, 19))
    elif
        return leng

def moveSnake(leng, xs, ys, v):
    for i in range(leng):
        x[i+1]=x[i]

    if(v == 0):
        ys[0] = ys[0] - 1
    elif(v == 1):
        xs[0] = xs[0] + 1
    elif(v == 2):
        ys[0] = ys[0] + 1
    elif(v == 3):
        xs[0] = xs[0] - 1




#def vec_conv
def main():


    HOST = '127.0.0.1'  # The remote host
    PORT = 9500         # The same port as used by the server


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Connection with matrix


        # Snake
        xs = [4, 5, 6]
        ys = [5, 5, 5]
        leng = 2
        f = (random.randint(0, 9), random.randint(0, 19))
        v = 2
        game = True
        while game:
            clock.tick(5)
            for e in pygame.evcent.get():
        		if e.type == QUIT:
        			sys.exit(0)
        		elif e.type == KEYDOWN:
        			if   e.key == K_UP    and v != 0:
                        v = 2
        			elif e.key == K_DOWN  and v != 2:
                        v = 0
        			elif e.key == K_LEFT  and v != 1:
                        v = 3
        			elif e.key == K_RIGHT and v != 3:
                        v = 1
            if(checkCollisionWalls(xs, ys) or checkSelfCollision(ys, xs, leng)):
                game = False
            else:
                leng = checkEatSnake(xs, ys, leng, f)
                moveSnake(leng, xs, ys, v)
                updateScreen(xs, ys, leng, f, s)

# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
