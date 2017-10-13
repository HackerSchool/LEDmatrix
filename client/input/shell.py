from sys import stdin
from msvcrt import getch

class Shell:
    def __init__(self, input_queue):
        self.input_queue = input_queue
        #self.bindings = ['Select', 'Start', 'Up', 'Down', 'Left', 'Right', 'A', 'B']
        self.bindings = {'K': 'Select', 'L': 'Start', 'W': 'Up', 'S': 'Down', 'A': 'Left', 'D':'Right', 'I': 'A', 'O': 'B'}
        
        # no need to find the keyboard (i hope)

        self.loop()

    def read(self):
        # with this function you have to press enter everytime you give an input
        while True:
            d = stdin.readline().rstrip().upper()   # this is not necessary because is a keyboard input, but why not?
            if d and d in self.bindings:
                #print("got: " + d)
                return d[0], self.bindings[d[0]]

    def read2(self):
        # with this function you DONT have to press enter everytime you give an input
        # just press and go! (but have the problem of exiting the program NEEDS FIX)
        while True:
            raw_d = getch()

            if raw_d == b'\x03': # keyboard interruption 
                exit()

            d = raw_d.decode("utf-8").upper()
            #print(d)
            if d in self.bindings:
                return d[0], self.bindings[d[0]]



    def loop(self):
        while True:
            act, btn = self.read2()
            #print("btn is: " + btn)
            if act == 'R':
                continue
            self.input_queue.put(btn)