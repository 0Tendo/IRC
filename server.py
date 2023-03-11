




## Main Program ##

# try initiate conn on a socket
try:
    print('Connecting to server...')
    client.connect((HOST, PORT))
except:
    sys.exit(f'Error: Failed to connect!\nhost: {HOST} \nport: {PORT}.')

print(f'Connected!')