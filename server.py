#server side program for internet relay chat program
#handles multiple connections

import socket
import select

HOST = '127.0.0.1'
PORT = 8080
HEADER_LEN = 11

opcodes = {
    'IRC_OC_ERR': b'\x01',
    'IRC_OC_SEND_MSG': b'\x02',
    'IRC_OC_RCV_MSG': b'\x03',
    'IRC_OC_ENTER': b'\x04',
    'IRC_OC_EXIT': b'\x05',
}

# create server socket object and set socket options
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

# become a server socket and listen for incoming connections
server.listen()

# create list of sockets server initiall - clients added as they join
user_list = [server]

# dictionary of clients
client_list = {}

# function to receive messages from clients
def receive_msg(client):
    try:
        # First receive message header
        msg_header = client.recv(HEADER_LEN)
        # If no header received, assume client has disconnected
        if not msg_header:
            return False
        # Parse message length from header
        msg_length = int(msg_header.decode('utf-8').strip())
        # Extract opcode from message header
        opcode = msg_header[HEADER_LEN:].decode('utf-8').strip()
        # Receive message data and return as dictionary
        return {'header': msg_header, 'opcode': opcode, 'data': client.recv(msg_length).strip()}

    # If an error occurs during message receive, assume client has disconnected
    except:
        return False

# main loop to handle incoming messages
while True:
    # use select() to wait for input from sockets
    read_sockets, _, exception_sockets = select.select(user_list, [], user_list)

    # loop through sockets with input
    for universal_socket in read_sockets:
        # if the input socket is the server socket, accept the connection
        if universal_socket == server:
            # accept new client connection and receive initial username message
            client, client_address = server.accept()
            user = receive_msg(client)
            # if no message received or error occurred, continue waiting for input
            if user is False:
                continue
            # add client socket to list of sockets and add client to dictionary of connected clients
            user_list.append(client)
            client_list[client] = user
            # print connection information to console
            print(f'New connection from {client_address[0]}:{client_address[1]} username: {user["data"].decode("utf-8")}')
        else:
            # receive message from connected client
            msg = receive_msg(universal_socket)
            # if no message received or error occurred, assume client has disconnected
            if msg is False:
                # print disconnection information to console and remove client from lists/dictionaries
                print(f'Closed connection from {client_list[universal_socket]["data"].decode("utf-8")}')
                user_list.remove(universal_socket)
                del client_list[universal_socket]
                continue
            # get sending client's information from dictionary
            user = client_list[universal_socket]
            # print received message information to console
            print(f'Received message from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')
            # loop through connected clients (excluding the sending client) and send the received message
            for client in client_list:
                if client != universal_socket:
                    client.send(user['header'] + user['data'] + msg['header'] + msg['data'])

    # loop through sockets with exceptions (e.g. errors or disconnections)
    for universal_socket in exception_sockets:
        # remove the socket from the list of sockets and dictionary of clients
        user_list.remove(universal_socket)
        del client_list[universal_socket]