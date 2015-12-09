#!/usr/bin/env python

import getpass
import sys
import telnetlib
import socket

HOST = "localhost"

print "starting telnet.py"

portn = 6571
tn = telnetlib.Telnet(HOST,portn)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 6666))

while True:
        dataFromClient, address = server_socket.recvfrom(256)
        print dataFromClient
        tn.write(dataFromClient)
