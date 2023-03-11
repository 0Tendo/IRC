#client side program for internet relay chat program

import socket
import sys
import select
import errno

HOST = '173.255.245.163'
PORT = 8080
BUFFER_SIZE = 102400 
HEADER_LEN = 10           
USERNAME = 'undefined_user'     

# assign username
username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to server
client.connect((HOST, PORT))
client.setblocking(False)

username_header = f"{len(username):<{HEADER_LEN}}".encode('utf-8')
client.send(username_header + username.encode('utf-8'))

while True:
    # send messages
    message = input(f'{username} > ')

    # check if message is not empty
    if message:
        message_header = f"{len(message):<{HEADER_LEN}}".encode('utf-8')
        client.send(message_header + message.encode('utf-8'))

    try:
        while True:
            # receive messages
            username_header = client.recv(HEADER_LEN)
            if not len(username_header):
                print('Connection error. Server closed.')
                sys.exit()

            user_len = int(username_header.decode('utf-8').strip())
            username = client.recv(user_len).decode('utf-8')

            message_header = client.recv(HEADER_LEN)
            message_length = int(message_header.decode('utf-8').strip())
            message = client.recv(message_length).decode('utf-8')

            print(f'{username} : {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()

