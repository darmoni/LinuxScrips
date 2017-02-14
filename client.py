#!/usr/bin/env python
 
import socket
 
 
TCP_IP = '127.0.0.1'
PORT = 50007

BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
 
print "received data:", data
