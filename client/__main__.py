import socket
import sys
from threading import Thread
from queue import Queue
from client.const import *

def main(args):
    try:
        input_module = args[2]
    except IndexError:
        input_module = 'hesv1'

    exec('from client.input.{0} import {1} as Input'.format(input_module,
            input_module.capitalize()), globals())
    try:
        input_method = Input()
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    input_queue = Queue()
    input_thread = Thread(target=input_method.loop, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    matrix = socket.socket(socket.AF_UNIX)
    matrix.connect(SOCK_PATH)

    try:
        app = args[1]
    except IndexError:
        app = 'menu'

    exec('from client.apps.{0} import {1} as App'.format(app,
            app.capitalize()), globals())
    App(matrix, input_queue)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
