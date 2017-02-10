import sys
import serial
import time
import socket

def xy_convert_vertical(x, y):

    if y % 2 != 0:
        return (y*10 + x)
    else:
        return (y*10 + 9 - x)

def xy_convert_horizontal( x, y):

     if x % 2 == 0:
         return (x*10 + y)
     else:
         return (x*10 + 9 - y)
#def vec_conv
def main():
  li = []

  li.extend(range(0, 600))
  for i in range(600):
      li[i] = 0
  ser = serial.Serial('/dev/cu.usbmodemFD121',115200);
  #for i in range(10):
  #just to clean buffer and matrix
  for i in range(10):
      ser.write(bytearray(li))
      time.sleep(0.5);

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("go listen")
    conn, addr = s.accept()
    print("accept")
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(data)
            if not data: break
            conn.sendall(data)
while 1:

      i = input("What is led to change ?")
      r = input("RED: ")
      g = input("GREEN: ")
      b = input("BLUE: ")
      li[3*int(i)] = int(r);
      li[3*int(i)+1] = int(g);
      li[3*int(i)+2] = int(b);
      ser.write(bytearray(li))
ser.close()
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
