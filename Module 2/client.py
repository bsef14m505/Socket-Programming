import socket               # Import socket module
from thread import *

s = socket.socket()         
host = socket.gethostname()
port = 5188                # Reserve a port for your service.
s.connect((host, port))

def client(null):
	while True:
		data= s.recv(1024)
		if data=='Disconnection':
                        #print "Some User has Disconnected\n"
                        s.send('Disconnection')
		elif not(data.endswith('Disconnection*')):
                        print str(data)
		
start_new_thread(client, (0,))
#s.send('nothing')
while True:
	reply = raw_input()
        s.send(reply)
	if reply=='exit()' or reply=="quit()":
                break
s.close                     # Close the socket when done
