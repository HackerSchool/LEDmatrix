import socket
import time
def main():

    HOST = '127.0.0.1'  # The remote host
    PORT = 9500         # The same port as used by the server

    G = [[0 for x in range(5)] for y in range(5)]
    G[0][0] = 1
    G[0][1] = 1
    G[0][2] = 1
    G[0][3] = 0
    G[0][4] = 0
    G[1][0] = 1
    G[1][1] = 0
    G[1][2] = 0
    G[1][3] = 0
    G[1][4] = 0
    G[2][0] = 1
    G[2][1] = 0
    G[2][2] = 1
    G[2][3] = 1
    G[2][4] = 0
    G[3][0] = 1
    G[3][1] = 0
    G[3][2] = 0
    G[3][3] = 1
    G[3][4] = 0
    G[4][0] = 1
    G[4][1] = 1
    G[4][2] = 1
    G[4][3] = 1
    G[4][4] = 0
    r = [[0 for x in range(10)] for y in range(20)]
    g = [[0 for x in range(10)] for y in range(20)]
    b = [[0 for x in range(10)] for y in range(20)]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        init_x = 3
        init_y = 0
        while True:
            for i in range(20):
                for j in range(10):
                    r[i][j]=0
                    g[i][j]=0
                    b[i][j]=0
            #r = input("R:")
            #g = input("G:")
            #b = input("B:")


            # for j in range(200):
            #     i = i + r + "|"
            #     i = i + g + "|"
            #     i = i + b + "|"
            #
            for i in range(5):
                for j in range(5):
                    r[i+init_y][j+init_x]=G[i][j] * 255


            mensage = ""
            for j in range(20):
                for i in range(10):
                    mensage = mensage + str(r[j][i]) + "|"
                    mensage = mensage + str(g[j][i]) + "|"
                    mensage = mensage + str(b[j][i]) + "|"

            s.sendall(mensage.encode('UTF-8'))
            init_y = init_y + 1
            time.sleep(0.5);


if __name__ == '__main__':
    main()
