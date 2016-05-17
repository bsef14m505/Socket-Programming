'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *

con=[]
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5188 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def serverfunc(conn):
        #Sending message to connected client
    conn.send('Welcome to the server. Press Enter to send message\r\nTerminating Commands: "exit()" and "quit()"\r') #send only takes string
    if conn==con[0]:
        conn.send('\n\t\t\tYou are User 1\r\n')
    else:
        conn.send('\n\t\t\tYou are User 2\r\n')
    while True:
        data = conn.recv(1024)
        if conn==con[0]:            
            con[1].send("User 1:"+data+'*')
        elif conn==con[1]:
            con[0].send("User 2:"+data+'*')
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    con.append(conn)
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(serverfunc ,(conn,))
 
s.close()
