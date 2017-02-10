import sys
import serial


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

  li.extend(range(0, 10))
  li[0] = 0xFFFFFF
  li[1] = 0xFFFFFF
  li[2] = 0xFFFFFF
  li[3] = 0xFFFFFF
  li[4] = 0xFFFFFF
  li[5] = 0x000000
  li[6] = 0xFFFFFF
  li[7] = 0xFFFFFF
  li[8] = 0xFFFFFF
  li[9] = 0xFFFFFF
  ser = serial.Serial('/dev/ttyUSB0',115200);
  for i in range(10):
    ser.write(li[i])

  ser.close()
# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
