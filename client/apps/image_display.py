import socket
from queue import Queue
from PIL import Image
from argparse import ArgumentParser

from client.const import *


class ImageDisplay:
    def __init__(self, matrix, input_queue):
        self.s = matrix
        self.input_queue = input_queue  # useless?

        self.table = [[(0, 0, 0)] * WIDTH for _ in range(HEIGHT)]
        
        self.clear()

    def clear(self, color=(0, 0, 0)):
        self.table = [[color] * WIDTH for _ in range(HEIGHT)]
        self.update_screen()

    def update_screen(self):
        frame = b''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                frame += bytes(self.table[i][j])
        
        self.s.sendall(frame)

    def load_image(self, input_file, rotate=None):
        img = Image.open(input_file)
        if 'P' in img.mode:  # check if image is a palette type
            img = img.convert("RGB")  # convert it to RGB

        if rotate:
            img = img.rotate(rotate)  # PIL.Image.FLIP_LEFT , PIL.Image.ROTATE_90

        img.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)  # regular resize

        for line in range(len(list(img.getdata())) // WIDTH):
            self.table[line] = list(img.getdata())[line * WIDTH : line * WIDTH + WIDTH]

    def print_image(self, input_file, background=(0, 0, 0), rotate=None):

        self.table = [[background] * WIDTH for _ in range(HEIGHT)]
        self.load_image(input_file, rotate=rotate)
        self.update_screen()


if __name__ == '__main__':

    parser = ArgumentParser(description='LED Matrix image display.', prog='ledmatrix imagedisplay')
    parser.add_argument('-f', '--file', default=None)
    parser.add_argument('-b', '--background', default=(0, 0, 0))  # placeholder, this argument is useless for now
    parser.add_argument('-r', '--rotate', default=0)  # degrees to rotate
    args = parser.parse_args()

    if args.file:
        matrix_socket = socket.socket()
        matrix_socket.connect(('localhost', PORT))

        ImageDisplay(matrix_socket, Queue()).print_image(args.file, args.background, int(args.rotate))
    else:
        raise AttributeError("No filename given")

    # img.paste(self, im, box=None, mask=None), useful for background?
    # img.tobytes(self, encoder_name='raw', *args)

    # img.save(newSourceFile, quality = 95, dpi=(72,72), optimize = True)
    # set quality, dpi , and shrink size
