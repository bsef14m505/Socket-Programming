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
def clientthread(conn):
        #Sending message to connected client
    conn.send('Welcome to the server. Type something and press "." to send message and "q" to exit\r') #send only takes string
    while True:
        if conn==con[0]:
            conn.send('\n\t\t\tYou are User 1\r\n')
            reply='\r\nUser 1:'
            #infinite loop so that function do not terminate and thread do not end.
            while True:
                 
                #Receiving from client
                data = con[0].recv(2048)
                reply =reply + data
                if data=='q' or data=='Q': 
                    break
                elif data=='.':
                    conn.send('\r\n')
                    con[1].send(reply+'\r\n')
                    #conn.send('\n\rUser 1:')
                    reply='User 1:'
                #con[1].send(reply)
                    
            #came out of loop
            conn.close()
            con[0].close()
           # con.remove(0)
            break
        elif conn==con[1]:
            conn.send('\n\t\t\tYou are User 2\r\n')
            reply='\r\nUser 2:'
            #infinite loop so that function do not terminate and thread do not end.
            while True:
             
                #Receiving from client
                data = con[1].recv(2048)
                reply =reply + data
                if data=='q' or data=='Q': 
                    break
                elif data=='.':
                    conn.send('\r\n')
                    con[0].send(reply+'\r\n')
                   # conn.send('\n\rUser 2:')
                    reply='User 2:'
                    
            #came out of loop
            conn.close()
            con[1].close()
            #con.remove(1)
            break
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    con.append(conn)
    print con
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
