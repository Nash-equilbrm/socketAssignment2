import threading
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import sys
import socket
import tkinter.messagebox as mbox 
from myFunction import*

PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '127.0.0.1'
# ADDR = (SERVER, PORT)
DISCONNECT = "!DISCONNECT"
SIGN_IN = "SIGN IN"
SIGN_UP = "SIGN UP"
DOWNLOAD ="DOWNLOAD"
SEARCH = "SEARCH"
READ = "READ"
LIMIT_USER_AMOUNT ="LIMITED USER AMOUNT"
ACK_USER ="ACK USER"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

index = None   
username = ''

TITLE = "LOGIN"

def PlaceWindow(window, window_width, window_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

def CloseWindow(root):
    root.destroy()

def Function():
    
    def Logout():
        global username
        username = ''
        RootFunction.destroy()
        main()

    def Search():
        for i in tree.get_children():
            tree.delete(i)
        try:
            send(client,SEARCH)
            search_command = SearchBox.get('1.0','end-1c')
            send(client,search_command)
            reply = recv(client)
            if reply == "Invalid Syntax":
                mbox.showinfo(None,"Invalid Syntax!")
            else:
                length = int(reply)
                for i in range(length):
                    info = recv(client)
                    info = info.split("_")
                    tree.insert('', 'end', iid= i, text="" , values=(str(i+1),info[1],info[0],info[2],info[4],info[3]))
        except Exception:
            mbox.showinfo(None,'Server mất kết nối!')
            


                        
    def SelectFunction(event):
        def ReadBook():    
            def Back():
                CloseWindow(RootRead)
                FunctionChoosen.set("Chọn chức năng") 
            
            def OpenBook():
                try:
                    send(client,READ)
                    Book_id = BookIDInput.get('1.0','end-1c')
                    send(client,Book_id)
                    response = recv(client)
                    if response == 'Book found!':
                        sz = recv(client)
                        sz = int(sz)
                        byte_read=0
                        data =b''
                        BookContent.configure(state='normal')
                        BookContent.delete('1.0','end')
                        while byte_read < sz:
                            data += client.recv(2)
                            byte_read+=2
                        data = data.decode(FORMAT)
                        BookContent.insert('end',data)
                        BookContent.configure(state='disabled')
                    else:
                        mbox.showinfo(None,"Book ID not found!")
                except Exception:
                    mbox.showinfo(None,'Server mất kết nối!')


            RootRead = Toplevel(RootFunction)
            RootRead.grab_set()
            RootRead.title(220*' '+"Đọc sách")
            PlaceWindow(RootRead, 1500, 800)
            RootRead.resizable(0, 0)

            #BackToMenu
            BackButton = Button(RootRead, text = "Trở lại", command = Back)
            BackButton.place(x= 20, y = 20, width = 100)

            #Input BookID
            BookIDInput = Text(RootRead)
            BookIDInput.insert('end',"Nhập ID sách....")
            BookIDInput.place(x = 20, y = 70, width = 800, height = 20)

            #Input ID Button
            InputIDButton = Button(RootRead, text = "Xem sách", command = OpenBook)
            InputIDButton.place(x= 830, y = 70, width = 200)
        
            #BookContent
            BookContent = Text(RootRead)
            BookContent.configure(state='disabled')
            BookContent.place(x = 20, y = 110, width = 1450, height = 650)
            vsb = ttk.Scrollbar(RootRead, command=BookContent.yview)
            vsb.place(x = 1470, y = 110, height =650)



        def DownloadBook():
            def Back():
                CloseWindow(RootDownload)
                FunctionChoosen.set("Chọn chức năng") 
            global file_extension  
            file_extension = '0'
             
            def Download():
                try:
                    send(client,DOWNLOAD)
                    Book_id = BookIDInput.get('1.0','end-1c')
                    send(client,Book_id)
                    send(client, file_extension)

                    response = recv(client)
                    if response != 'Book found!':
                        mbox.showinfo(None,response)
                    else:
                        book_name = recv(client)
                        sz = recv(client)
                        sz = int(sz)
                        byte_read = 0
                        data = b''
                        DownloadProgress.configure(state = 'normal')
                        with open(book_name+file_extension,'wb') as f:
                            while byte_read < sz:
                                data += client.recv(2)
                                byte_read += 2

                                DownloadProgress.delete("1.0", "end")
                                
                                DownloadProgress.tag_configure("center", justify='center')
                                DownloadProgress.insert(1.0, "Đang tải "+str(int(byte_read/sz*100)) + " %")                #insert % here
                                DownloadProgress.tag_add("center", "1.0", "end")
                                
                            
                            f.write(data)
                        DownloadProgress.configure(state = 'disable')
                        mbox.showinfo(None,"Download complete!")
                except Exception:
                    mbox.showinfo(None,'Server mất kết nối!')

            
            

            def SelectType(event):
                global file_extension
                s= TypeChoosen.get()
                if  s == " .txt": file_extension = '.txt'
                if  s == " .doc": file_extension = '.doc'
                if  s == " .docx": file_extension = '.docx'
                if  s == " .pdf": file_extension = '.pdf'

            RootDownload = Toplevel(RootFunction)
            RootDownload.grab_set()
            RootDownload.title(80*' '+"Tải sách")
            PlaceWindow(RootDownload, 600, 300)
            RootDownload.resizable(0, 0)
            
            #BackToMenu
            BackButton = Button(RootDownload, text = "Trở lại", command = Back)
            BackButton.place(x= 20, y = 20, width = 100)

            #Input BookID
            BookIDInput = Text(RootDownload)
            BookIDInput.insert('end',"Nhập ID sách....")
            BookIDInput.place(x = 20, y = 70, width = 400, height = 20)

            #Type 
            TypeChoosen = ttk.Combobox(RootDownload,state="readonly")
            TypeChoosen.set("Chọn định dạng") 
            TypeChoosen['values'] = (' .txt',' .doc',' .docx',' .pdf')
            TypeChoosen.place(x = 430, y = 70, width = 150)
            TypeChoosen.bind('<<ComboboxSelected>>', SelectType)

            #Input ID Button
            InputIDButton = Button(RootDownload, text = "Tải sách", command = Download)
            InputIDButton.place(x= 205, y = 120, width = 170)

            #DownloadProgress
            DownloadProgress = Text(RootDownload)
            DownloadProgress.configure(state = 'disable')
            DownloadProgress.place(x = 100, y = 200, width = 400, height  = 20)


        s= FunctionChoosen.get()
        if  s == " Đọc sách": ReadBook()
        if  s == " Tải sách": DownloadBook()
   

    RootFunction = Tk()
    RootFunction.title(220*' '+"MENU")
    PlaceWindow(RootFunction, 1500, 700)
    RootFunction.resizable(0, 0)

    #Library Label
    LibraryLabel = Text(RootFunction, bd = 0)
    LibraryLabel.insert('end',80*" "+"ONLINE LIBRARY")
    LibraryLabel.configure(state='disabled')
    LibraryLabel.place(x = 20, y = 20, height = 20, width = 1460)

    #HelloLabel
    
    HelloLabel = Label(RootFunction, text = "Xin chào " + username)
    HelloLabel.place(x = 1000-username.__len__(), y = 50)

    #LogoutButton
    SearchButton = Button(RootFunction, text ="Đăng xuất", command = Logout)
    SearchButton.place(x=1300, y = 50, width = 180)
    
    #ChooseFunction
    FunctionChoosen = ttk.Combobox(RootFunction,state="readonly")
    FunctionChoosen.set("Chọn chức năng") 
    FunctionChoosen['values'] = (' Đọc sách',' Tải sách')
    FunctionChoosen.place(x = 20, y = 60, width = 200)
    FunctionChoosen.bind('<<ComboboxSelected>>', SelectFunction)

    #SearchBook
    SearchBox = Text(RootFunction)
    SearchBox.insert('end',"Tra cứu tại đây...")
    SearchBox.place(x = 20, y = 100, height = 20, width = 1200)

    #SearchButton
    SearchButton = Button(RootFunction, text ="Tra cứu", command = Search)
    SearchButton.place(x=1250, y = 100, width = 230)


    #TableBook
    tree =ttk.Treeview(RootFunction, column=("c1", "c2", "c3","c4","c5","c6"), show='headings')
    vsb = ttk.Scrollbar(RootFunction, orient="vertical", command=tree.yview)

    tree.bind('<Button-1>', "break")
   
    tree.column("#1", anchor=tk.CENTER, minwidth=0, width=50, stretch= FALSE)
    tree.heading("#1", text="STT")
    tree.column("#2", anchor=tk.CENTER, minwidth=0, width=450 ,stretch=FALSE)
    tree.heading("#2", text="Tên sách")
    tree.column("#3", anchor=tk.CENTER, minwidth=0, width=150, stretch=FALSE)
    tree.heading("#3", text="ID")
    tree.column("#4", anchor=tk.CENTER, minwidth=0, width=350, stretch=FALSE)
    tree.heading("#4", text="Tác giả")
    tree.column("#5", anchor=tk.CENTER, minwidth=0, width=300, stretch=FALSE)
    tree.heading("#5", text="Loại sách")
    tree.column("#6", anchor=tk.CENTER, minwidth=0, width=140, stretch=FALSE)
    tree.heading("#6", text="Năm sáng tác")
    tree.place(x = 20, y = 150, height = 520)
    vsb.place(x=20+50+450+150+350+300+140, y=150, height=520)
    
    
def __init__window(Client_windows):
    global index
    def Login():
        def LoginCheck():
            global username
            #check
            try:
                send(client,SIGN_IN)
                username = usernameEntry.get()
                password =passwordEntry.get()
                
                
                send(client,username)
                send(client,password)
                reply = recv(client)
                if reply == "Sign in successfully!":
                    LoginSuccessful()

                else:
                    LoginFail()
            except Exception:
                mbox.showinfo(None,'Server mất kết nối!')
            
            
        def LoginFail():
            RootLoginFail = Toplevel(Client_windows)
            RootLoginFail.grab_set()

            RootLoginFail.title(10*' '+"Lỗi đăng nhập")
            PlaceWindow(RootLoginFail, 300, 180)

            FailLabel = Label(RootLoginFail, text = "Tài khoản hoặc mật khẩu của bạn không chính xác!\n Vui lòng nhập lại")
            FailLabel.place(x=10, y = 40)
            OkButton = Button(RootLoginFail, text = "OK",command = lambda: CloseWindow(RootLoginFail))
            OkButton.place(x = 85, y = 110, width = 130)

        def LoginSuccessful():
            RootLoginS = Toplevel(Client_windows)
            RootLoginS.grab_set()

            RootLoginS.title(10*' '+"Đăng nhập")
            PlaceWindow(RootLoginS, 300, 180)

            FailLabel = Label(RootLoginS, text = "Đăng nhập thành công! \n Nhấn OK để tiếp tục")
            FailLabel.place(x= 90, y = 40)
            OkButton = Button(RootLoginS, text = "OK",command = lambda: [CloseWindow(Client_windows),Function()])
            OkButton.place(x = 85, y = 110, width = 130)
            
        
        LoginCheck()

    def Register():
        
        def checkRegistry():
            global username
            #check
            try:
                send(client,SIGN_UP)
                username = usernameEntry.get()
                password = passwordEntry.get()
                send(client,username)
                send(client,password)
                reply = recv(client)
                if reply == "Sign up successfully!":
                    RegisterSuccessful()
                else:
                    RegisterFail()
            except Exception:
                mbox.showinfo(None,'Server mất kết nối!')

        def RegisterSuccessful():
            RootRS = Toplevel(RootRegister)
            RootRS.grab_set()
            RootRS.title(10*' '+"Thông báo")
            PlaceWindow(RootRS, 300, 150)

            SuccessfulLabel = Label(RootRS, text = "Đăng kí thành công!")
            SuccessfulLabel.place(x=100, y = 30)
            OkButton = Button(RootRS, text = "OK",command = lambda: [CloseWindow(RootRS),CloseWindow(RootRegister)])
            OkButton.place(x = 85, y = 80, width = 130)

        def RegisterFail():
            RootRF = Toplevel(RootRegister)
            RootRF.grab_set()
            RootRF.title(10*' '+"Thông báo")
            PlaceWindow(RootRF, 300, 150)

            SuccessfulLabel = Label(RootRF, text = "Username của bạn đã tồn tại!\n Vui lòng đăng ký lại")
            SuccessfulLabel.place(x=80, y = 30)
            OkButton = Button(RootRF, text = "OK",command = lambda: CloseWindow(RootRF))
            OkButton.place(x = 85, y = 80, width = 130)
        

        
        RootRegister = Toplevel(Client_windows)
        RootRegister.grab_set()

        RootRegister.title(30*' '+"Đăng ký tài khoản")
        PlaceWindow(RootRegister, 400, 150)

        usernameLabel = Label(RootRegister, text = "Username: ")
        usernameLabel.place(x = 30, y = 10)
        usernameEntry = Entry(RootRegister)
        usernameEntry.place(x= 130, y = 10, width = 200)

        passwordLabel = Label(RootRegister, text = "Password: ")
        passwordLabel.place(x = 30, y = 50)
        passwordEntry = Entry(RootRegister)
        passwordEntry.place(x= 130, y = 50, width = 200)

        #checkButton
        OkButton = Button(RootRegister, text = "OK",command = checkRegistry)
        OkButton.place(x = 140, y = 95, width = 130)

    def End():
        global index
        try:
            send(client,DISCONNECT)
            send(client,str(index))
            sys.exit(1)
        except Exception:
            sys.exit(1)

        

    #init window
    Client_windows.title(80*" "+TITLE)
    PlaceWindow(Client_windows, 600, 400)
    Client_windows.resizable(0, 0)

    #label Library
    Label_Library = Text(Client_windows, bd = 0)
    Label_Library.place(x = 200, y = 60, width = 200, height = 20)
    Label_Library.insert('end',6*" "+"ONLINE LIBRARY")
    Label_Library.configure(state='disabled')

    #username va password
    usernameLabel = Label(Client_windows, text = "Username: ")
    usernameLabel.place(x = 100, y = 140)

    usernameEntry = Entry(Client_windows)
    usernameEntry.place(x= 200, y = 140, width = 200)

    passwordLabel = Label(Client_windows, text = "Password: ")
    passwordLabel.place(x = 100, y = 190)

    passwordEntry = Entry(Client_windows)
    passwordEntry.place(x= 200, y = 190, width = 200)

    #Dang nhap, dang ki
    LoginButton = Button(Client_windows, text = "Đăng nhập", command= Login)
    # LoginButton.bind("<Button-1>",Login)
    LoginButton.place(x = 320, y = 250, width = 80)

    RegisterButton = Button(Client_windows, text = "Đăng ký", command= Register)
    RegisterButton.place(x = 200, y = 250, width = 80)

    EndButton = Button(Client_windows, text = "Kết thúc", command= End)
    EndButton.place(x = 200, y = 300, width = 200)    

def main():     
    Client_windows = Tk()
    __init__window(Client_windows)
    Client_windows.mainloop()

def IPConnect():
    global index
    def ConnectSuccessful():
        CloseWindow(ConnectIP)
        main()
    def Connect():
        global index
        IP_addr = IPInput.get('1.0','end-1c')
        ADDR = (IP_addr,PORT)
        try:
            client.connect(ADDR)
            msg = recv(client)
            if msg == ACK_USER:
                index = recv(client)
                index = int(index)
                ConnectSuccessful()
            else:
                mbox.showinfo(None,"Quá giới hạn số lượng người dùng!")
                sys.exit(1)
        except Exception as e:
            mbox.showinfo(None,"Không thể kết nối đến server!")
            print(e)


        
    
    ConnectIP = Tk()
    ConnectIP.title(50*" "+"Connect")
    PlaceWindow(ConnectIP, 400, 200)
    ConnectIP.resizable(0, 0)
    
    #IPInput
    IPInput = Text(ConnectIP)
    IPInput.insert("end","Nhập ip server ...")
    IPInput.place (x = 20, y = 50, width = 360, height = 20)

    #ConnectButton 
    ConnectButton = Button(ConnectIP, text = "Kết nối", command = Connect)
    ConnectButton.place(x = 150, y = 100, width = 100)

    ConnectIP.mainloop()




IPConnect()