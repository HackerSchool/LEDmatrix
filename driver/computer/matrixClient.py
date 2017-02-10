import socket

def main():

    HOST = '127.0.0.1'  # The remote host
    PORT = 50007              # The same port as used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(b'Hello, world')
            data = s.recv(1024)

if __name__ == '__main__':
    main()
