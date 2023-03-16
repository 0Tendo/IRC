#a basic client for an IRC chatroom
#this is the client side of the chatroom
import socket  # For creating sockets
import select  # For monitoring sockets
import sys     # For exiting program
import threading


HOST = '127.0.0.1'  
PORT = 8080         
SOCKET_LIST = []   
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
    # Create a new socket for IPv4 and TCP connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set socket option to reuse the address to avoid "address already in use" errors
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Connect to the server using the predefined HOST and PORT
    server.connect((HOST, PORT))

    # Create a new thread to handle receiving messages from the server
    recv_thread = threading.Thread(target=receive_message, args=(server,))
    # Set the thread to run as a daemon, allowing the main program to exit even if the thread is still running
    recv_thread.daemon = True
    # Start the thread
    recv_thread.start()

    # Continuously read user input
    while True:
        try:
            # Get user input and remove any leading/trailing whitespace
            data = input().strip()
            # Check if the user input is not empty
            if data:
                # Check if the user input starts with "/list"
                if data.startswith('/list'):
                    # Send the LIST command to the server
                    server.send('LIST\n'.encode('utf-8'))
                # Check if the user input starts with "/nick"
                elif data.startswith('/nick'):
                    # Send the NICK command with the new nickname to the server
                    server.send(('NICK ' + data[6:]).encode('utf-8'))
                # Check if the user input starts with "/join"
                elif data.startswith('/join'):
                    # Send the JOIN command with the room name to the server
                    server.send(('JOIN ' + data[6:]).encode('utf-8'))
                # Check if the user input starts with "/quit"
                elif data.startswith('/quit'):
                    # Send the QUIT command to the server
                    server.send('QUIT\n'.encode('utf-8'))
                    # Break the loop to exit the program
                    break
                    # Exit the program
                    sys.exit()
                # If the user input doesn't start with a command
                else:
                    # Assume that any input without a command prefix is a message
                    # Send the MSG command with the message to the server
                    server.send(('MSG ' + data).encode('utf-8'))
        # If an exception occurs (e.g., keyboard interrupt), continue the loop
        except:
            continue

    # Close the socket when the loop ends
    server.close()

# Execute the main function if the script is run as a standalone program
if __name__ == "__main__":
    main()

