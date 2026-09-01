import threading
import socket
import time

n=4
mid=0
clock=0
s="relese"
deferred=set()
received=set()
myreq=None
lock=threading.Lock()
PORTS = {
    0: 6000,
    1: 6001,
    2: 6002,
    3: 6003
}
def sendmess(addr,messa):
    sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sc.connect(addr)
    sc.send(messa)
    sc.close()
def reqc():
    global mid
    global s
    global clock
    global received
    global myreq
    with lock:
        s="REQUEST"
        clock+=1
        myreq=(clock,mid)
        t=clock
        received.clear()
    for i in range(n):
        if i!=mid:
            sendmess(("127.0.0.1",PORTS[i]),f"REQUEST|{t}|{mid}")
    while True:
        with lock:
            if len(received)==n-1:
                break
    entercs()
def entercs():
    global s
    with lock:
        s="entered"
    time.sleep(1)
    relese()
def relese():
    global s
    global myreq
    with lock:
        s="relese"
        myreq=None
        pending=list(deferred)
        deferred.clear()
    for i in pending:
        sendmess(("127.0.0.1",PORTS[i]),f"REPLY|{mid}")
def handlereq(t,pid):
    global clock
    with lock:
        clock=max(clock,t)+1
        req= (t,pid)
        if s=="entered":
            deferred.add(pid)
            return
        elif s=="REQUEST":
            if req>myreq:
                deferred.add(pid)
                return 
    sendmess(("127.0.0.1",PORTS[pid]),f"REPLY|{mid}")
def receive():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(("127.0.0.1", PORTS[mid]))
    server.listen()
    while True:
        client,add=server.accept()
        mess=client.recv(1024).decode()
        client.close()
        #received.add(mess)
        p=mess.split('|')
        if p[0]=="REQUEST":
            handlereq(p[1],p[2])
        elif p[0]=="REPLY":
            with lock:
                received.add(p[1])
thread=threading.Thread(target=receive)
thread.start()
while True:
    c=int(input("1-enter cs 2-exit"))
    if c==1:
        reqc()
    elif c==2:
        break
