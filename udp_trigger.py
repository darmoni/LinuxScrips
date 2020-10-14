#!/usr/bin/env python3
from socket import socket, AF_INET, SOCK_DGRAM

PORT = 12345
sock = socket(AF_INET,SOCK_DGRAM)
msg = "Hello UDP server"
for counter in range(3):
    sock.sendto(msg.encode('utf-8'),('38.102.250.167', PORT))
  