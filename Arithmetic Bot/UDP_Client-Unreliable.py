from socket import *
import sys

lines = []
# Read the file argument
try:
    with open(sys.argv[1]) as file:
        lines = file.readlines()
except IndexError:
    print("Missing required argument")

serverName = '127.0.0.1'
serverPort = 50001

for line in lines:
    #print(f"n\Client sending {line}")
    status_code = None
    clientSocket = socket(AF_INET, SOCK_DGRAM) # UDP type
    reply = None
    serverAddress = None
    d = 0.1
    while d <= 2:
        try:
            clientSocket.sendto(line.encode(),(serverName, serverPort))
            clientSocket.settimeout(d)
            #print("receiving...")
            while(serverAddress == None):
                reply, serverAddress = clientSocket.recvfrom(2048)
            #print('received')
            break
        except timeout:
            #print("timeout!")
            d = d*2
            if d > 2:
                print("Request timed out: the server is dead")
                status_code = 300
                break
            else:
                print("Request timed out: resending")
            pass
            
    if status_code == 300:
        print(f'Error {status_code}: the server is dead')
        clientSocket.close
        continue
    status_code, result = reply.decode().split()
    status_code = int(status_code)
    if status_code == 200:
        print(f'Result is {result}')
    elif status_code == 620:
        print(f'Error {status_code}: Invalid OC')
    elif status_code == 630:
        print(f'Error {status_code}: Invalid operands')
    clientSocket.close()
