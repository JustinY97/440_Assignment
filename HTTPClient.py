from datetime import *
from socket import *
import sys
from xmlrpc import server


args = sys.argv
BUFFER_SIZE = 4096
timeInfo = ("%s, %s %s %s %s %s" %(datetime.now().strftime('%a'), datetime.now().strftime('%d'), datetime.now().strftime('%b'), datetime.now().strftime('%Y'), datetime.now().strftime("%H:%M:%S"), datetime.now(timezone.utc).astimezone().tzname()))

# Checking number of arguments
if(len(args) > 4 or len(args) < 2 ):
    print("Usage: python HTTPClient.py hostname port")
    exit()

# If len(args) = 3, we are doing a GET request
if len(args) == 3:
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
        path = "/"
        try:
            path = path + args[1].split("/", 1)[1]
        except:
            path = "/"
        
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((hostname, int(port)))
    #clientSocket.connect(("www.cnn.com", 80))

    host = str("%s:%s" %(hostname, port))
    request = ("GET %s HTTP/1.1\r\nHost: %s\r\nTime: %s\r\nClass-name: VCU-CMSC440-2022\r\nUser-name: justinyork\r\n\r\n" % (path, host, timeInfo))
    print(request)
    clientSocket.sendall(request.encode())
    
    response = clientSocket.recv(BUFFER_SIZE)
    print(response.decode())
    
    

    clientSocket.close()

# Only other option is PUT
else:
    if args[1] == 'PUT':
        url = args[2]
        path = args[3]
        filename = path.split()[-1]
        print(filename)
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.connect((url, 1039))
        
        putRequest = ("PUT %s HTTP/1.1\r\nHost: %s\r\nTime: %s\r\nClass-name: VCU-CMSC440-2022\r\nUser-name: justinyork\r\n\r\n" % (path, url, timeInfo))
        print(putRequest)
        serverSocket.sendall(putRequest.encode())
        with open(path, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    #If no bytes left
                    return_message =serverSocket.recv(BUFFER_SIZE).decode()
                    print(return_message)
                    break
                
                serverSocket.sendall(bytes_read)

        serverSocket.close()

    
    else:
        print("Usage: python HTTPClient.py [PUT] URL [PATH/FILENAME]")
        exit()