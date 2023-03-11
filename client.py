#client side program for internet relay chat program

import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024 * 100            
USERNAME = 'undefined_user'     


## Main Program ##

# establish connection
try:
    print('Connecting to server...')
    client.connect((HOST, PORT))
except:
    sys.exit(f'Error: Failed to connect!\nhost: {HOST} \nport: {PORT}.')

print(f'Connected!')