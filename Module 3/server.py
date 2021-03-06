'''
    Simple socket server using threads
'''

import socket
import sys
from thread import *

con = []
name1 = []
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 5188  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'


# Function for handling connections. This will be used to create threads
def serverfunc(conn):
    while True:
        try:
            data = conn.recv(1024)
            print data
            for i in range(len(name1)):
                if data.startswith(name1[i] + ':'):
                    con[i].send(name1[con.index(conn)] + ":" + data[len(name1[i]) + 1:] + "\n")

        except socket.error as error:
            var = con.index(conn)
            del con[var]
            del name1[var]
            strn='A User Has Disconnected\nAvailable users are:\n\n'
            for i in range(len(name1)):
                strn=strn+name1[i]+'\n'
            print strn
            for i in range(len(name1)):
                con[i].send(strn)
            break


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    con.append(conn)
    name1.append(conn.recv(1024))
    strn='A User Has Connected\nAvailable users are:\n\n'
    for i in range(len(name1)):
        strn = strn + name1[i] + '\n'
    print strn
    for i in range(len(name1)):
        con[i].send(strn)
    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(serverfunc, (conn,))

s.close()
