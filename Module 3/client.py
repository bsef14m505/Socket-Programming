import socket  # Import socket module
from thread import *
from Tkinter import *
from threading import Thread, Lock
import tkMessageBox

mutex=Lock()

s = socket.socket()
host = socket.gethostname()
port = 5188  # Reserve a port for your service.
s.connect((host, port))

def quit1(event2):
    caller1=event2.widget
    input1=caller1.get('1.0','end-1c')
    mutex.acquire()
    try:
        s.send(input1)
    finally:
        mutex.release()
    login.destroy()

def retrieve_input(event1):
    text6=event1.widget
    input=text6.get('1.0','end-1c')
    text6.delete('0.0', END)
    mutex.acquire()
    try:
        s.send(input)
    finally:
        mutex.release()
    text6.delete("%s-1c" % INSERT, INSERT)


login=Tk(className=" LOGIN")
login.geometry('300x120')
login.resizable( width = False , height = False )
l = Label(login,text = "Enter Username" ,fg = 'black'  ,bg ='orange')
l.place(x=2,y=2,width=290,height=20)
txt11=Text(login,bg='white')
txt11.place(x=4,y=25,width=280,height=100)
txt11.bind( '<Return>' ,quit1)
login.mainloop()


root=Tk(className=" Client")
root.geometry('700x800')
root.resizable( width = False , height = False )

def devinfo():
   tkMessageBox.showinfo("Developer Information","Name: Muhammad Abdul Raheem\nRoll No: BSEF14M505")
B1 = Button(root, text = "Developer Information",fg='black',bg='orange',command = devinfo)
B1.pack()

class DrawBottomFrame:
    def __init__ ( self , root):
        fm = Frame(root, bg = "green" )
        fm.place( x = 300 , y = 550 , width = 399 , height = 249 )
        text_place = Text(fm, bg = "white" )
        text_place.place( x = 5 , y = 5 , width = 390 , height = 239 )
        text_place.bind( '<Return>' , retrieve_input)

center_frame = Frame(root, bg = "black" )
center_frame.place( x = 300 , y = 30 , width = 399 , height = 545)

bottom = DrawBottomFrame(root)

left1 = Frame(root, bg="blue")
left1.place(x=5, y=25, width=290, height=770)

def client(null):
    while True:
       # mutex.acquire()
        #try:
        data = s.recv(100000)
        if data.startswith('A User Has Connected') or data.startswith('A User Has Disconnected'):
            if data.startswith('A User Has Connected'):
                lb1=Label(left1,text=str(data),bg='Green')
            else:
                lb1=Label(left1,text=str(data),bg='Red')
            lb1.pack(fill=X)
            print "IF: "+data
        else:
            print "Else: "+ data
            lb1=Label(center_frame,text=str(data),bg='grey')
            lb1.pack(fill=X)
        #finally:
         #   mutex.release()
count=1
if count==1:
    start_new_thread(client, (0,))
    count=0
root.mainloop()
