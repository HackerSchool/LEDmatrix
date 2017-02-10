import sys

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

def main():
  

# this is the standard boilerplate that calls the main() function
if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
