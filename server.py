import socket 
import threading
import json
import os
import tkinter.messagebox as mbox 
from tkinter import*
from myFunction import*
from sign_in_up import *
from lookUp import*



PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
DISCONNECT = "!DISCONNECT"
SIGN_IN = "SIGN IN"
SIGN_UP = "SIGN UP"
DOWNLOAD ="DOWNLOAD"
SEARCH = "SEARCH"
READ = "READ"
LIMIT_USER_AMOUNT ="LIMITED USER AMOUNT"
ACK_USER ="ACK USER"


MAX_USER = None
all_connections ={}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)



def handle_client(conn, addr):
    global all_connections
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = recv(conn)
        
        

        if msg == SIGN_IN:
            username = recv(conn)
            
            password = recv(conn)
            
            if SignIn(username,password) == True:
                send(conn,"Sign in successfully!")
            else:
                send(conn,"Sign in failed!")
        elif msg ==SIGN_UP:
            username = recv(conn)
            password = recv(conn)
            if SignIn(username,password) == True:
                send(conn,"Account already exists!")
            elif SignUp(username,password) == True:
                send(conn,"Sign up successfully!")
            else:
                send( conn,"Sign up failed!")
        elif msg == SEARCH:
            search_command = recv(conn)
            if valid_command(search_command):
                cmd,arg = get_param(search_command)
                result = search_results(cmd,arg)
                length = len(result)
                send(conn,str(length))
                for book in result:
                    info = str(book[0]) + "_" + book[1] + "_" +book[2] + "_" + str(book[3]) + "_"+ book[4]
                    send(conn,info)
            else:
                send(conn,"Invalid Syntax")


        elif msg == READ:
            Book_id = recv(conn)
            dir = book_directory(Book_id,'.txt')
            try:
                with open(dir,'rb') as f:
                    send(conn,'Book found!')
                    sz = f.seek(0,os.SEEK_END)
                    send(conn,str(sz))
                    f.seek(0,os.SEEK_SET)
                    while f.tell()< sz:
                        data = f.read(2)
                        conn.send(data)
            except FileNotFoundError:
                send(conn,'Book ID not found!')
            
    

        elif msg == DOWNLOAD:
            Book_id = recv(conn)
            file_extension = recv(conn)
            if(file_extension == '0'):
                send(conn,'Please choose file extension!')
            else:
                try:
                    with open("BOOKS.json",'r') as file:
                        data = json.load(file)
                        i=1
                        for book in data:
                            
                            check_id = str(data[book].get("id"))
                            
                            
                            if(check_id == Book_id):
                                if(data[book].get("extension").get(file_extension) == 1):
                                    send(conn,'Book found!')
                                    book_name = data[book].get("name")
                                    send(conn,book_name)
                                    dir = book_directory(Book_id,file_extension)
                                    with open(dir,'rb') as f:
                                        sz = f.seek(0,os.SEEK_END)
                                        send(conn,str(sz))
                                        f.seek(0,os.SEEK_SET)
                                        while f.tell()< sz:
                                            data = f.read(2)
                                            conn.send(data)

                                else:
                                    send(conn,'File type not available right now!')
                                break

                            i += 1
                            if (i > len(data)):
                                send(conn,'Book ID not found!')
                                

                            
                except FileNotFoundError:
                    print("An error occurs on database system!")


        elif msg == DISCONNECT:
            index = recv(conn)
            if len(all_connections) >0:
                del all_connections[index]
            connected = False

        elif msg =='':
            msg = "Connection Lost!" 
            connected =False
        
        
        print(f"[{addr}] {msg}")
            

    conn.close()
    conn = None
    


def start():
    global all_connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        all_connections.update({str(len(all_connections)):conn})
        if len(all_connections) > MAX_USER:
            send(conn,LIMIT_USER_AMOUNT)
            conn.close()
            conn = None
            del all_connections[str(len(all_connections)-1)]
        else:
            send(conn,ACK_USER)
            send(conn,str(len(all_connections)-1))
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}") #Trừ đi mainthread và thread dành cho openserver




def PlaceWindow(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def OpenServer():
    global MAX_USER
    MAX_USER =0
    try:
        MAX_USER = int(LimitUser.get())
        if MAX_USER < 0:
            mbox.showinfo(None,"Nhập giới hạn số lượng người dùng bị lỗi! Nhập lại")
        else:
            LimitUser.config(state="disabled")
            server.bind(ADDR)
            print("[STARTING] server is starting...")
            start()
    except Exception:
        mbox.showinfo(None,"Nhập giới hạn số lượng người dùng bị lỗi! Nhập lại")

def OpenServerThread():
    thread = threading.Thread(target= OpenServer)
    thread.start()

def CloseServer():
    global all_connections
    for connection in all_connections:
        all_connections[connection].close()
        all_connections[connection] = None
    all_connections.clear()
    all_connections =None
    os._exit(0)
    


RootServer = Tk()
RootServer.title(50*" "+"Server")
PlaceWindow(RootServer,400,200)

#OpenButton
OpenServerButton = Button(RootServer, text = "Mở Server",command = OpenServerThread)
OpenServerButton.place(x = 30, y = 20, width = 150, height = 70 )

#CloseButton
CloseServerButton = Button(RootServer, text = "Đóng Server",command = CloseServer)
CloseServerButton.place(x = 220, y = 20, width = 150, height = 70 )

#Limited users amount
LimitUserLabel =Label(RootServer, text= "Giới hạn ")
LimitUserLabel.place(x = 50, y = 110)
LimitUserLabel2 = Label (RootServer, text = "người dùng.")
LimitUserLabel2.place(x = 165, y = 110)
LimitUser = Entry(RootServer)
LimitUser.place(x= 110, y = 110, height= 20, width= 50)

#IPServer
IPServer = Text(RootServer)
IPServer. insert('end',"IP của Server: " + SERVER)
IPServer.place(x = 50, y = 150, height = 20, width = 300)

RootServer.mainloop()
