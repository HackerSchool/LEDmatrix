import random

def checkCollision(x, y):
    if x>=0 and x<10 and x>=0 and x<20:
        return false
    else:
        return true

while True:
    clock.tick(25)
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
