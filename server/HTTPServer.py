'''
Programmer: Justin York
Date: 04/24/2022
Description: Server program for sockets project!
'''
import os
from socket import *
import sys

BUFFER_SIZE = 1024
args = sys.argv
if len(args) != 2:
    print("Usage: python HTTPServer.py port")
    exit()

try:
    port = int(args[1])
except:
    print("ERR: - arg 2")
    exit()

#Create Welcoming Socket using port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', port))
serverSocket.listen(5)


print("Listening on port: %d ..." % port)
try:
    while True:
        conn, addr = serverSocket.accept()

        #setting a timeout just in case coed hangs up
        conn.settimeout(30)

        print("[SERVER] Client made connection...")
        print("%s:%d" % (addr[0], addr[1]))

        clientSentence = conn.recv(BUFFER_SIZE).decode()
        if clientSentence[0:3] == "GET":

            print("[CLIENT] %s" % clientSentence)

            file = clientSentence.split("HTTP/1.1")[0]
            file = file.strip("GET")
            file = file.strip()

            try:
                f = open(file)
            except:
                conn.send("[SERVER] ERR: File Not Found.")
                continue
            serverSentence = f.read()
            
            conn.send(serverSentence.encode())

        elif clientSentence[0:3] == "PUT":

            print("[CLIENT] %s" % clientSentence)

            clientSentence = clientSentence.split("HTTP/1.1")[0]
            clientSentence = clientSentence.strip("PUT")
            clientSentence = clientSentence.strip()

            arguments = clientSentence.split("/")

            if len(arguments) == 1:
                filename = arguments[0]
                filepath = "./"
            else:
                filename = arguments.pop()
                filepath = "/".join(arguments)

            conn.send(("Creating File: %s" % filename).encode())

            if not os.path.exists(filepath):
                    os.makedirs(filepath)       
            
            with open(os.path.join(filepath,filename), "w") as f:
                
                bytes_read = conn.recv(BUFFER_SIZE).decode() 
                f.write(bytes_read)

            #Check if file was created
            if os.path.exists(os.path.join(filepath, filename)):
                print("[SERVER] STATUS 200: OK File %s created." % filename)   
                conn.send(("[SERVER] STATUS 200: OK File %s created." %filename).encode())
            else:
                conn.send(b"[SERVER] STATUS 600: FAILED File NOT Created")
                    
                    
        else:
            serverSentence = "INVALID SYNTAX" 
            conn.send(serverSentence.encode())

        conn.close()
except KeyboardInterrupt:
    print("\n[SERVER] Keyboard Interupt Detected. Shutting down socket..")
    serverSocket.close()
    exit()