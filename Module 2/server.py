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
    var1=0
        #Sending message to connected client
    conn.send('Welcome to the server. Press Enter to send message\r\nTerminating Commands: "exit()" and "quit()"\r') #send only takes string
    conn.send("You are now User "+str(con.index(conn)+1)+"\nTotal Users connected are: \n")
    for i in range(len(con)):
        conn.send(con[i].recv(1024)+"\n")
    while True:
        data=conn.recv(1024)
        #print data
        if data=='exit()' or data=='quit()':
            print "User "+str(con.index(conn)+1)+" is disconnected\n"
            for i in range(len(con)):
                   # if i<>con.index(conn):
                con[i].sendall("User "+str(con.index(conn)+1)+" is disconnected\n")
                #con[i].sendall('Disconnection')
            del con[con.index(conn)]
            for i in range(len(con)):
                   # if i<>con.index(conn):
                #con[i].sendall("User "+str(con.index(conn)+1)+" is disconnected\n")
                con[i].sendall('Disconnection')    
           
           #conn.sendall('Disconnection')
                        
            var1=0
            #print "Disconnected from the server\nThe Communication won't be possible now.\n"
            break
        else:
            #data='Disconnection'
            #data = conn.recv(1024)
            if data=='Disconnection':
                conn.send("You are now User "+str(con.index(conn)+1)+"\nTotal Users connected are: \n")
                for i in range(len(con)):
                    conn.send(con[i].recv(1024)+"\n")
               #var1=1
            
            #if conn==con[0]:            
            con[con.index(conn)].send("User "+str(con.index(conn)+1)+":"+data+'*')
            #elif conn==con[1]:
            #   con[0].send("User 2:"+data+'*')
        
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    con.append(conn)
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(serverfunc ,(conn,))
 
s.close()
