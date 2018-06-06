import socket


def main():
    host = '127.0.0.1'
    port = 53910

    s = socket.socket()
    s.connect((host, port))

    message = input("-> ")

    while message.lower() != 'exit':
        s.sendall(message.encode())
        data = s.recv(5117).decode()
        print('Received from server: \n' + data)
        message = input("-> ")
    s.close()

if __name__ == '__main__':
    main()
