#a basic server for an IRC chatroom
#this is the server side of the chatroom

import socket
import select
import time

# Set server address and port
HOST = '127.0.0.1'
PORT = 8080

# Set up a list of sockets to keep track of all connected clients
SOCKET_LIST = []
RECV_BUFFER = 4096
CHATROOM = {}
NICKNAMES = {}


# Set up server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket option to allow reuse of address in case of restart
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to specified address and port
server.bind((HOST, PORT))

# Start listening for incoming connections, with a maximum backlog of 10 connections
server.listen(10)

# Add server socket to list of sockets to listen for incoming data
SOCKET_LIST.append(server)

# Define functions for each opcode

# Join a chatroom
def join_chatroom(client, data):
    if client in CHATROOM:
        client.send(b'You are already in a chatroom')
    else:
        CHATROOM[client] = data
        client.send(b'You have joined the chatroom: ' + data.encode('utf-8'))

# Leave a chatroom
def leave_chatroom(client, data):
    if client in CHATROOM:
        del CHATROOM[client]
        client.send(b'You have left the chatroom: ' + data.encode('utf-8'))
    else:
        client.send(b'You are not in a chatroom')

# Send a message to all clients in a chatroom
def send_message(client, data):
    if client in CHATROOM:
        for sock in SOCKET_LIST:
            if sock != server and sock != client:
                # Use NICKNAMES to get the sender's nickname
                sender = NICKNAMES.get(client, "Anonymous")
                message = sender + ': ' + data
                sock.send(message.encode('utf-8'))
    else:
        client.send(b'You are not in a chatroom')

# List all chatrooms
def list_chatrooms(client, data):
    if CHATROOM:
        chatroom_list = 'Chatrooms: ' + ', '.join(set(CHATROOM.values()))
        client.send(chatroom_list.encode('utf-8'))
    else:
        client.send(b'There are no chatrooms')

# Change nickname
def change_nick(client, data):
    NICKNAMES[client] = data
    client.send(b'Your nickname is now: ' + data.encode('utf-8'))

# Quit chatroom
def quit(client, data):
    client.send(b'You have quit the chatroom')
    SOCKET_LIST.remove(client)
    client.close()
    if client in CHATROOM:
        del CHATROOM[client]

# Send error message
def error(client, data):
    client.send(b'Error: ' + data)

# Define opcodes (commands) for the chatroom
opcodes = {
    'JOIN': join_chatroom,
    'LEAVE': leave_chatroom,
    'MSG': send_message,
    'LIST': list_chatrooms,
    'NICK': change_nick,
    'QUIT': quit,
    'ERROR': error,
}

# Parse received data to determine opcode and call appropriate function
def parse_data(client, data):
    if not data:
        # Handle empty data
        return
    try:
        opcode, data = data.decode('utf-8').split(' ', 1)
    except ValueError:
        opcode = data.strip()
        data = None

    if not opcode:
        # Handle empty opcode
        client.send(b'Error: Invalid opcode')
    else:
        try:
            opcodes[opcode](client, data)
        except KeyError:
            client.send(b'Error: Invalid opcode')

# Continuously listen for incoming connections and data
def main():
    while True:
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            if sock == server:
                sockfd, addr = server.accept()
                SOCKET_LIST.append(sockfd)
                print('Client (%s, %s) connected' % addr)
                sockfd.send('Welcome to the chatroom'.encode('utf-8'))

            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        parse_data(sock, data)
                except:
                    # Handle client disconnect
                    print("Client (%s, %s) disconnected" % sock.getpeername())
                    sock.close()
                    SOCKET_LIST.remove(sock)
                    if sock in CHATROOM:
                        del CHATROOM[sock]

        time.sleep(0.1)

if __name__ == "__main__":
    main()



