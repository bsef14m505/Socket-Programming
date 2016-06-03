'''
    Simple socket server using threads
'''
 
import socket
import sys
from thread import *

con=[]
name1=[]
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
    conn.send('Welcome to the server. Press Enter to send message\r\nTerminating Commands: "exit()" and "quit()"\r\nTo ADD Users, Command: "add()"\r\nTo REMOVE Users, Command: "remove()"\r\n') #send only takes string
    name2=[]
    while True:
        try:
            data = conn.recv(1024)
            var3=0
            if data=='add()':
                conn.send('\n\nSelect Your User\nAvailable users are:\n')
                for j in range(len(name1)):
                    conn.send(str(j+1)+": "+name1[j]+"\n")
                data = conn.recv(1024)
                a=data
                if int(a)>0 and int(a)<=len(name1):                    
                    name2.append(name1[int(a)-1])
                    data = conn.recv(1024)
                else:
                    conn.send("\nInvalid User Number\n")
            elif data=='remove()':
                conn.send('\n\nSelect Your User to remove\nAdded users are:\n')
                for j in range(len(name2)):
                    conn.send(str(j+1)+": "+name2[j]+"\n")
                data = conn.recv(1024)
                var3=1
                a=data
                if int(a)>0 and int(a)<=len(name2):                    
                    del name2[int(a)-1]
                else:
                    conn.send("\nInvalid User Number\n")
            var2=0
            for i in range(len(name1)):
                if data.startswith(name1[i]+':'):
                    con[i].send(name1[con.index(conn)]+":"+data[len(name1[i])+1:]+"\n")
                    var2=1 
            if var2==0 and var3==0:
                for i in range(len(name2)):
                        con[name1.index(name2[i])].send(name1[con.index(conn)]+": "+data)
                        
        except socket.error as error:
            var=con.index(conn)
            del con[var]
            del name1[var]
            print "Connected Users: "
            print name1
            for i in range(len(name1)):
                con[i].send('\n\nA User has disconnected\nAvailable users are:\n')
                for j in range(len(name1)):
                    con[i].send(name1[j]+"\n")
            break
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    con.append(conn)
    name1.append(conn.recv(1024))
    for i in range(len(name1)):
        con[i].send('\n\nA User has connected\nAvailable users are:\n')
        for j in range(len(name1)):
            con[i].send(name1[j]+"\n")
    print "Connected Users: "
    print name1
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(serverfunc ,(conn,))
 
s.close()
