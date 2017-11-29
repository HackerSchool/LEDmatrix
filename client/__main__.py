"""
Client initialization code.
It opens the selected input module and the matrix socket.

It then runs a matrix app, by default the 'menu' app,
passing it the matrix object (just a regular socket object)
and the input_queue object (just a regular Queue).

It imports the input_module and the app directly by their
provided name, so it must match a filename. From those
files it imports a class with the same name except
the first letter is capitalized.
The class is then instantiated with two arguments,
(matrix, input_queue).
"""

from argparse import ArgumentParser
import socket
import sys
from threading import Thread
from queue import Queue
from client.const import *

DEFAULT_INPUT = 'hesv1'
DEFAULT_APP = 'menu'

def main(app, input_module):
    # e.g. if input_module == 'controller', we exec:
    # 'from client.input.controller import Controller as Input'
    # and then instantiate the class Controller (in another thread),
    # with one argument (input_queue)
    exec('from client.input.{0} import {1} as Input'.format(input_module,
            input_module.capitalize()), globals())
    try:
        input_queue = Queue()
        input_thread = Thread(target=Input, args=(input_queue,))
        input_thread.daemon = True
        input_thread.start()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    matrix = socket.socket()
    matrix.connect(('localhost', PORT))

    # e.g. if app == 'test', we exec:
    # 'from client.apps.test import Test as App'
    # and then instantiate the class Test,
    # with two arguments (matrix, input_queue)
    exec('from client.apps.{0} import {1} as App'.format(app,
            app.capitalize()), globals())
    App(matrix, input_queue)


if __name__ == '__main__':
    parser = ArgumentParser(description='LED Matrix client.', prog='ledmatrix_client')
    parser.add_argument('-a', '--app', default=DEFAULT_APP)
    parser.add_argument('-i', '--input', default=DEFAULT_INPUT)
    args = parser.parse_args()
    main(args.app, args.input)
