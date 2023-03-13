import socket
import sys
import errno

# server: 173.255.245.163
HOST = '127.0.0.1'
PORT = 8080
HEADER_LEN = 11
USERNAME = 'undefined_user'

# assign username
username = input("Enter your username: ")

# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.setblocking(False)

# encode username and opcode fields for message header
username_bytes = username.encode('utf-8')
opcode_bytes = b'\x00' # initialize opcode to 0

while True:
    # send messages
    message = input(f'{username} > ')

    # check if message is not empty
    if message:
        # encode message and update length and opcode fields in message header
        message_bytes = message.encode('utf-8')
        length_bytes = f"{len(username_bytes) + len(opcode_bytes) + len(message_bytes):<{HEADER_LEN}}".encode('utf-8')
        header_bytes = length_bytes + opcode_bytes
        
        # send message header and message payload to server
        client.sendall(header_bytes + username_bytes + message_bytes)

    try:
        while True:
            # receive messages
            header = client.recv(HEADER_LEN + 1) # receive entire header (length field + opcode field)
            if not len(header):
                print('Connection error. Server closed.')
                sys.exit()

            # extract opcode field from message header
            opcode = header[-1]
            
            # extract username and message data from received bytes
            username_header = client.recv(HEADER_LEN)
            username_length = int(username_header.decode('utf-8').strip())
            username = client.recv(username_length).decode('utf-8')

            message_header = client.recv(HEADER_LEN)
            message_length = int(message_header.decode('utf-8').strip()) - 1 # subtract 1 to exclude opcode byte
            message = client.recv(message_length).decode('utf-8')

            # print message with opcode field included
            print(f'Opcode {opcode}: {username} : {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
