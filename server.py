import socket 
import threading
import json
import os
from tkinter import*
from myFunction import*
from sign_in_up import *
from lookUp import*
# C:\Users\MSI-NK\OneDrive\Máy tính\Tai_lieu_Socket_th\DoAnSocketTH


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
SIGN_IN = "SIGN IN"
SIGN_UP = "SIGN UP"
DOWNLOAD ="DOWNLOAD"
SEARCH = "SEARCH"
READ = "READ"






server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = recv(conn)
        
        if msg == DISCONNECT_MESSAGE:
            
            connected = False

        elif msg == SIGN_IN:
            username = recv(conn)
            
            password = recv(conn)
            
            if SignIn(username,password) == True:
                send(conn,"Sign in successfully!")
            else:
                send(conn,"Sign in failed!")
        elif msg ==SIGN_UP:
            username = recv(conn)
            password = recv(conn)
            if SignUp(username,password) == True:
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


            
        elif msg =='':
            msg = "Connection Lost!" 
            connected =False
        
        
        print(f"[{addr}] {msg}")
            

    conn.close()
    
all_connections =[]
def start():
    global all_connections
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        all_connections.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}") #Trừ đi mainthread và thread dành cho openserver

# print("[STARTING] server is starting...")
# start()


def PlaceWindow(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def OpenServer():
    server.bind(ADDR)
    print("[STARTING] server is starting...")
    start()

def OpenServerThread():
    thread = threading.Thread(target= OpenServer)
    thread.start()

def CloseServer():
    global all_connections
    for i,conn in enumerate(all_connections):
        conn.close()
    os._exit(0)
    


RootServer = Tk()
RootServer.title(50*" "+"Server")
PlaceWindow(RootServer,400,200)

#OpenButton
OpenServerButton = Button(RootServer, text = "Mở Server",command = OpenServerThread)
OpenServerButton.place(x = 30, y = 20, width = 150, height = 70 )

#OpenButton
CloseServerButton = Button(RootServer, text = "Đóng Server",command = CloseServer)
CloseServerButton.place(x = 220, y = 20, width = 150, height = 70 )

#IPServer
IPServer = Text(RootServer)
IPServer. insert('end',"IP của Server: " + SERVER)
IPServer.place(x = 50, y = 130, height = 20, width = 300)

RootServer.mainloop()
