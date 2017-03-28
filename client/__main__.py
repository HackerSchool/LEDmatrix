from argparse import ArgumentParser
import socket
import sys
from threading import Thread
from queue import Queue
from client.const import *


DEFAULT_INPUT = 'hesv1'
DEFAULT_APP = 'menu'


def main(app, input_module):
    exec('from client.input.{0} import {1} as Input'.format(input_module,
            input_module.capitalize()), globals())
    try:
        input_method = Input()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    input_queue = Queue()
    input_thread = Thread(target=input_method.loop, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    matrix = socket.socket()
    matrix.connect(('localhost', PORT))

    exec('from client.apps.{0} import {1} as App'.format(app,
            app.capitalize()), globals())
    App(matrix, input_queue)


if __name__ == '__main__':
    parser = ArgumentParser(description='LED Matrix client.', prog='ledmatrix_client')
    parser.add_argument('-a', '--app', default=DEFAULT_APP)
    parser.add_argument('-i', '--input', default=DEFAULT_INPUT)
    args = parser.parse_args()
    main(args.app, args.input)
