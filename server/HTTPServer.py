import os
from socket import *
import sys

BUFFER_SIZE = 1024
args = sys.argv
if len(args) != 2:
    print("Usage: python HTTPServer.py port")
    exit()
port = int(args[1])

#Create Welcoming Socket using port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', port))
serverSocket.listen()


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

            print(f"[CLIENT] {clientSentence}")

            file = clientSentence.split("HTTP/1.1")[0]
            file = file.strip("GET")
            file = file.strip()

            f = open(file)

            serverSentence = f.read()
            
            conn.send(serverSentence.encode())

        elif clientSentence[0:3] == "PUT":

            print(f"[CLIENT] {clientSentence}")

            clientSentence = clientSentence.strip("PUT ")
            
            arguments = clientSentence.split(" ")

            filepath = arguments[0]
            filename = arguments[1]

            conn.send(f"Creating File: {filename}".encode())

            if not os.path.exists(filepath):
                    os.mkdir(filepath)       
            
            with open(os.path.join(filepath,filename), "w") as f:
                
                bytes_read = conn.recv(BUFFER_SIZE).decode() 
                f.write(bytes_read)

            #Check if file was created
            if os.path.exists(os.path.join(filepath, filename)):
                print(f"[SERVER] STATUS 200: OK File {filename} created.")   
                conn.send(f"[SERVER] STATUS 200: OK File {filename} created.".encode())
            else:
                conn.send(b"STATUS 600: File Not Created")
                    
                    
        else:
            serverSentence = "INVALID SYNTAX" 
            conn.send(serverSentence.encode())

        conn.close()
except KeyboardInterrupt:
    print("\n[SERVER] Keyboard Interupt Detected. Shutting down socket..")
    serverSocket.close()
    exit()