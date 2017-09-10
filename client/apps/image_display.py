import time
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

    def update_screen(self):
        frame = b''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                frame += bytes(self.table[i][j])

        self.s.sendall(frame)

    def load_image(self, img, background_color=(0, 0, 0), rotate=None):
        img = img.copy()

        if 'P' in img.mode:  # check if image is a palette type
            img = img.convert('RGB')  # convert it to RGB

        if rotate:
            img = img.rotate(rotate)

        img.thumbnail((WIDTH, HEIGHT), Image.ANTIALIAS)  # resize

        final_img = Image.new('RGB', (WIDTH, HEIGHT), background_color)
        final_img.paste(img, (0, 0))

        for line in range(len(list(final_img.getdata())) // WIDTH):
            self.table[line] = list(final_img.getdata())[line * WIDTH : line * WIDTH + WIDTH]

    def print_image(self, input_file, background_color=(0, 0, 0), rotate=None, loop=False):
        frame = Image.open(input_file)
        frame_index = 0

        while frame:  # in case it's a sequence (GIF)
            self.clear()
            self.load_image(frame, background_color=background_color, rotate=rotate)
            self.update_screen()

            try:
                time.sleep(frame.info['duration']/1000)  # will fail if it's not a sequence

                frame_index += 1
                try:
                    frame.seek(frame_index)
                except EOFError:
                    if loop:
                        frame_index = 0
                        frame.seek(frame_index)
                    else:
                        break
            except KeyError:  # not a sequence, break the loop
                break


if __name__ == '__main__':

    parser = ArgumentParser(description='LED Matrix image display.', prog='ledmatrix imagedisplay')
    parser.add_argument('-f', '--file', default=None, type=str)
    parser.add_argument('-b', '--background', default=(0, 0, 0))  # placeholder, this argument is useless for now
    parser.add_argument('-r', '--rotate', default=0, type=int)  # degrees to rotate
    parser.add_argument('-l', '--loop', default=False, action='store_true')  # loop sequences?
    args = parser.parse_args()

    if args.file:
        matrix_socket = socket.socket()
        matrix_socket.connect(('localhost', PORT))

        ImageDisplay(matrix_socket, Queue()).print_image(args.file, args.background, int(args.rotate), args.loop)
    else:
        raise AttributeError('No filename given')

    # img.paste(self, im, box=None, mask=None), useful for background?
    # img.tobytes(self, encoder_name='raw', *args)

    # img.save(newSourceFile, quality = 95, dpi=(72,72), optimize = True)
    # set quality, dpi , and shrink size
