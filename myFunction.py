import os
HEADER = 64
FORMAT = "utf-8"

def send(conn,msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def recv(conn):
    msg =''
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    return msg

def getSize(filename):
    sz=0
    with open(filename) as file:
        file.seek(0,os.SEEK_END)
        sz = file.tell()
    return sz


def send_binary_file(conn,filename):
    sz = getSize(filename)
    hop = sz/2
    hop=int(hop)
    send(conn,str(sz))
    with open(filename,'rb') as file:
        for i in range(hop):
            data = file.read(2)
            conn.send(data)

def recv_binary_file(conn, filename):
    sz = recv(conn)
    sz = int(sz)
    hop = sz/2
    hop = int(hop)
    with open(filename,'wb') as file:
        for i in range(hop):
            data = conn.recv(2)
            file.write(data)



