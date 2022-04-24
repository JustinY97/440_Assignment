from datetime import *
from socket import *
import sys
import os



args = sys.argv
BUFFER_SIZE = 1024
SEPERATOR = "<SEPERATOR>"
timeInfo = ("%s, %s %s %s %s" %(datetime.now().strftime('%a'), datetime.now().strftime('%d'), datetime.now().strftime('%b'), datetime.now().strftime('%Y'), datetime.now().strftime("%H:%M:%S")))

# Checking number of arguments
if(len(args) > 4 or len(args) < 2 ):
    print("Usage: python HTTPClient.py [PUT] URL/ [FILEPATH]")
    exit()

# If len(args) = 2, we are doing a GET request
if len(args) == 2:

    #Strip off the http:// or https:// from the front
    args[1] = args[1].strip("http://")
    args[1] = args[1].strip("https://")

    # Check and see if there is a port number
    try:
        hostname = args[1].split(":")[0]

        # Split the port and path by "/" with a maximum number of splits of 1
        try:
            port = args[1].split(":")[1].split("/", 1)[0]
            path = args[1].split(":")[1].split("/", 1)[1]
        except:
            port = args[1].split(":")[1]
            path = "/"
            
    # If not port given use 80 as default
    except:
        print("No port given. Using default port 80")
        hostname = args[1].split("/", 1)[0]

        # Assign default port 80
        port = "80"
        path = "/"
        try:
            path = path + args[1].split("/", 1)[1]
        except:
            path = "/"
        
    
    #Create a client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostname, int(port)))

    host = str("%s:%s" %(hostname, port))
    request = ("GET %s HTTP/1.1\r\nHost: %s\r\nTime: %s\r\nClass-name: VCU-CMSC440-2022\r\nUser-name: justinyork\r\n\r\n" % (path, host, timeInfo))
    print(request)
    clientSocket.sendall(request.encode())
    
    response = clientSocket.recv(BUFFER_SIZE)
    print(response.decode())
    
    

    clientSocket.close()

# Only other option is PUT
elif args[1] == 'PUT':

    #Get URL and Port Number
    #Strip off the http:// or https:// from the front
    args[2] = args[2].strip("http://")
    args[2] = args[2].strip("https://")

    # Check and see if there is a port number
    try:
        hostname = args[2].split(":")[0]

        # Split the port and path by "/" with a maximum number of splits of 1
        try:
            port = args[2].split(":")[1].split("/", 1)[0]
            path = args[2].split(":")[1].split("/", 1)[1]
        except:
            port = args[2].split(":")[1]
            path = "/"
            
    except:
        print("No port given. Using default port 80")
        hostname = args[2].split("/", 1)[0]

        # Assign default port 80
        port = "80"
        path = "/"
        try:
            path = path + args[1].split("/", 1)[1]
        except:
            path = "/"

    #Get Filename and Filesize
    filepath = args[3]
    filename = filepath.split("/")[-1]
    filesize = os.path.getsize(filepath)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostname, int(port)))

    request = ("PUT %s HTTP/1.1\r\nHost: %s\r\nTime: %s\r\nClass-name: VCU-CMSC440-2022\r\nUser-name: justinyork\r\n\r\n" % ((path + "/" +filename), ":".join([hostname,port]), timeInfo))
    print(request)
    clientSocket.sendall(request.encode())
    
    #clientSocket.sendall(("PUT %s %s" % (path, filename)).encode())
    
    #Wait for response with filename
    msg = clientSocket.recv(BUFFER_SIZE).decode()
    print("[SERVER] %s" % msg)

    with open(args[3], "rb") as f:
        data = f.read()
        clientSocket.send(data)
            

    reply = clientSocket.recv(BUFFER_SIZE).decode()
    print(reply)

    clientSocket.close()
    

else:
    print("Usage: python HTTPClient.py [PUT] URL/ [FILEPATH]")
    exit()