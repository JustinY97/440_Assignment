from base64 import decode
from http import client
from socket import *
import sys

BUFFER_SIZE = 4096
args = sys.argv
if len(args) != 2:
    print("Usage: python HTTPServer.py port")
    exit()
port = int(args[1])

#Create Welcoming Socket using port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen()

print("Listening on port: %d ..." % port)
while 1:
    conn, addr = serverSocket.accept()
    print("Client made connection")
    print("%s:%d" %(addr[0], addr[1]))

    clientSentence = conn.recv(BUFFER_SIZE).decode()
    print("From Client...\n%s" % clientSentence)

    if clientSentence[0:3] == "GET":
        file = clientSentence.split("HTTP/1.1")[0]
        file = file.strip("GET")
        file = file.strip("/")
        file = file.strip()
        file = file.replace("/", "\\")

        f = open(file)
        serverSentence = f.read()
        
        conn.send(serverSentence.encode())

    if clientSentence[0:3] == "PUT":
        while True:
            bytes_read = conn.recv(BUFFER_SIZE) 
            if not bytes_read:
                conn.send(b"STATUS 200 OK")
                break
            print(bytes_read.decode())
    else:
        serverSentence = "Invalid Syntax" 
        conn.send(serverSentence.encode())

    conn.close()
    
serverSocket.close()