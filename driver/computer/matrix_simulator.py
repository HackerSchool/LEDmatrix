import sys, pygame
import socket
import threading
from multiprocessing import Queue


HOST = ''                # Symbolic name meaning all available interfaces
PORT = 9500              # Arbitrary non-privileged port
height = 20
width = 10
resolution_mult = 32  # Scaling factor so it doesn't actually take only 20x10 pixels on the screen

BLACK = 0, 0, 0
WHITE = 255, 255, 255


def receive_full_frame(connection) -> str:
    message = b''
    while True:
        # height*width pixels * 3 colors + height*width separators
        buf = connection.recv(height*width*3 + height*width) 
        message += buf
        if not buf:
            print('conn done')
            connection.close()
            return message

def parse_message(message: bytes):
    colors = message.decode("UTF-8").split("|")
    '''
    if len(colors) != height*width*3:
        print(len(colors))
        raise ValueError
    '''
    pixels = [[] for i in range(height*width)]
    for i, color in enumerate(colors):
        pixels[i//3].append(int(color))

    return pixels

def network_thread(HOST, PORT, queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)
        print("listening")

        while True:
            conn, addr = s.accept()
            print('Connected by', addr)

            message = receive_full_frame(conn)
            pixel_array = parse_message(message)
            queue.put(pixel_array)           


pygame.init()
screen = pygame.display.set_mode((width*resolution_mult, height*resolution_mult))
pygame.display.set_caption("LED Matrix simulation")

clock = pygame.time.Clock()

q = Queue()
thread = threading.Thread(target=network_thread, args=(HOST, PORT, q))
thread.daemon = True  # if the main thread exits the program won't keep running
thread.start()

while True:
    clock.tick(60)  # 60 fps

    for event in pygame.event.get():  # Necessary for the window close button to work 
        if event.type == pygame.QUIT: 
            sys.exit() 
    
    if not q.empty(): 
        screen.fill(BLACK)

        pixel_array = q.get()

        for i, pixel in enumerate(pixel_array):
            if not pixel: 
                break  # temporary    
            pygame.draw.rect(screen, 
                                (pixel[0], pixel[1], pixel[2]),  # pixel colors
                                (i%20*resolution_mult,  # pixel x location
                                 i//20*resolution_mult,  # pixel y location
                                 1*resolution_mult,  # pixel height 
                                 1*resolution_mult))  # pixel width

        pygame.display.flip()  # update the window
