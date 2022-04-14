from ast import arg
from socket import *
import sys

args = sys.argv

# If length of arguments is 1, we run GET
if(len(args) != 2):
    print("Usage: python HTTPClient.py hostname port")
else:
    args[1] = args[1].strip("http://")

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
        
    except:
        print("No port given. Using default port 80")
        hostname = args[1].split("/", 1)[0]

        # Assign default port 80
        port = "80"
        try:
            path = args[1].split("/", 1)[1]
        except:
            path = "/"
    
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostname, int(port)))
    #clientSocket.connect(("www.cnn.com", 80))
    host = str("%s:%s" %(hostname, port))
    clientSocket.sendall(("GET %s HTTP/1.1\r\nHost: %s" % (path, host)).encode())
    print(clientSocket.recv(4096))
    clientSocket.close()