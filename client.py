#a basic client for an IRC chatroom
#this is the client side of the chatroom
import socket  
import sys     
import threading


HOST = '127.0.0.1'  
PORT = 8080          
RECV_BUFFER = 4096 

opcodes = {
    0 : 'JOIN',
    1 : 'LEAVE',
    2 : 'MSG',
    3 : 'LIST',
    4 : 'NICK',
    5 : 'QUIT',
    6 : 'ERROR',
}


def receive_message(client):
    while True:
        data = client.recv(RECV_BUFFER)
        if not data:
            print('Disconnected from server')
            sys.exit()
        else:
            print(data.decode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect((HOST, PORT))

    recv_thread = threading.Thread(target=receive_message, args=(server,))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        try:
            data = input().strip()
            if data:
                if data.startswith('/list'):
                    server.send('LIST\n'.encode('utf-8'))
                elif data.startswith('/nick'):
                    server.send(('NICK ' + data[6:]).encode('utf-8'))
                elif data.startswith('/join'):
                    server.send(('JOIN ' + data[6:]).encode('utf-8'))
                elif data.startswith('/leave'):
                    server.send(('LEAVE ' + data[7:]).encode('utf-8'))
                elif data.startswith('/quit'):
                    server.send('QUIT\n'.encode('utf-8'))
                    break
                    sys.exit()
                elif data.startswith('/help'):
                    print('List of commands:\n/list\n/nick\n/join\n/leave\n/quit\n/help')
                else:
                    server.send(('MSG ' + data).encode('utf-8'))
        except:
            continue

    server.close()

if __name__ == "__main__":
    main()

