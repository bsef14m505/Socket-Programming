import socket               # Import socket module
from thread import *

s = socket.socket()         
host = socket.gethostname()
port = 5188                # Reserve a port for your service.
s.connect((host, port))

def client(null):
	while True:
		data= s.recv(1024)
		print str(data)
		
start_new_thread(client, (0,))

while True:
	reply = raw_input()
	if reply=='exit()' or reply=="quit()":
                break
	else:
                s.send(reply)
s.close                     # Close the socket when done
