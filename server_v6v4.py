#!/usr/bin/env python

# Echo server program
import socket
import sys

from threading import Thread
from SocketServer import ThreadingMixIn
 
class ClientThread(Thread):
 
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for "+ip+":"+str(port)
 
 
    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            print "received data:", data
            if "/bye" in data:
                conn.send("Bye. Please come again\n")
                break
                
            if "/version" in data:
                conn.send("Demo version\n")
                
            if "/echo" in data:
                data = data.replace("/echo","")
                conn.send(data + "\n")
                conn.send(data)  # echo
                
        conn.close()

HOST = 'localhost'               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.bind(sa)
        threads = []
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)

while True:
    s.listen(4)
    conn, addr = s.accept()
    print 'Connected by', addr
    if af == socket.AF_INET:
        ip, port = addr
    else:
        ip, port, f1, f2 = addr
    print "Waiting for incoming connections..."
    
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)
 
for t in threads:
    t.join()

conn.close()
