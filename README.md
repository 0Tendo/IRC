An command line interface (CLI) Internet Relay Chat (IRC) server and client I developed for PSU CS494P (Internetworking Protocols)

First, run the server so that clients can connect.

_python server.py_

Then, connect to the server with a client to begin chatting.

_python client.py_

The client is set to connect locally for demonstrative purposes but can be modified connect to any server!

Default HOST = '127.0.0.1'

Default PORT = 8080


Implemented features:

send messages to everyone in the current chat room

_*any message*_

change username

_/nick *desired username*_


join room

_/join *name of room*_


leave room

_/leave *name of room*_


list currently available rooms

_/list_


quit

_/quit_


Additional details are outlined in the attached RFC


