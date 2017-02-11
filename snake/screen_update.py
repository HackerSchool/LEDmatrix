
import socket
import time
#s - socket
#xs - snake x positions
#ys - snake y positions
#lenght - snake lenght
def update_screen(s,xs,ys,lenght,xf,yf):
    snake_color = {'R': 255 , 'G': 0, 'B': 0}
    food_color = {'R': 255 , 'G': 0, 'B': 0}
    w = 10
    h = 20
    r = [[0 for x in range(w)] for y in range(h)]
    g = [[0 for x in range(w)] for y in range(h)]
    b = [[0 for x in range(w)] for y in range(h)]
    for i in range(h):
        for j in range(w):
            r[i][j]=0
            g[i][j]=0
            b[i][j]=0

    for i in range(lenght):
        r[ys[i]][xs[i]] = snake_color['R']
        g[ys[i]][xs[i]] = snake_color['G']
        b[ys[i]][xs[i]] = snake_color['B']

    r[yf][xf] = snake_color['R']
    g[yf][xf] = snake_color['G']
    b[yf][xf] = snake_color['B']
    mensage = ""
    for j in range(h):
        for i in range(w):
            mensage = mensage + str(r[j][i]) + "|"
            mensage = mensage + str(g[j][i]) + "|"
            mensage = mensage + str(b[j][i]) + "|"

    s.sendall(mensage.encode('UTF-8'))


def main():

    HOST = '127.0.0.1'  # The remote host
    PORT = 9500         # The same port as used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        xs = [4,4,4]
        ys = [2,1,0]
        lenght = 3
        xf = 4
        yf = 18
        while True:
            update_screen(s,xs,ys,lenght,xf,yf)
        #    xf = int(input("new food x position"))
            #yf = int(input("new food y position"))
            time.sleep(1)

            for i in range(lenght-1):
                ys[i+1] = ys[i]
            ys[0]=ys[0]+1
if __name__ == '__main__':
    main()
