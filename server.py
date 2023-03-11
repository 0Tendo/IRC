#server side program for internet relay chat program

import socket
import select





## Main Program ##

HOST = '127.0.0.1'
PORT = 8080
BUFFER = 102400
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to a public host, and a well-known port
server.bind((HOST, PORT))

# become a server socket
server.listen()

# list of socket clients
user_list = [server]

client_list = {}


# a function to recieve message from client
def recieve_msg(client):
    try:
        msg_header = client.recv(BUFFER)
        if not len(msg_header):
            return False
        msg_length = int(msg_header.decode('utf-8'))
        return {'header': msg_header, 'data': client.recv(msg_length)}

    except:
        return False
    
# a list of input steams 
while True:
    read_sockets, _, exception_sockets = select.select(user_list, [], user_list)

    for notified_socket in read_sockets:
        if notified_socket == server:
            client, client_address = server.accept()
            user = recieve_msg(client)
            if user is False:
                continue
            user_list.append(client)
            client_list[client] = user
            print(f'New connection from {client_address[0]}:{client_address[1]} username: {user["data"].decode("utf-8")}')
        else:
            msg = recieve_msg(notified_socket)
            if msg is False:
                print(f'Closed connection from {client_list[notified_socket]["data"].decode("utf-8")}')
                user_list.remove(notified_socket)
                del client_list[notified_socket]
                continue
            user = client_list[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')
            for client in client_list:
                if client != notified_socket:
                    client.send(user['header'] + user['data'] + msg['header'] + msg['data'])
