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

for line in lines: # open and close socket for each line
    #print(f"n\Client sending {line}")
    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP type
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(line.encode())
    reply = clientSocket.recv(1024) # wait for reply
    status_code, result = reply.decode().split()
    status_code = int(status_code)
    if status_code == 200:
        print(f'Result is {result}')
    elif status_code == 620:
        print(f'Error {status_code}: Invalid OC')
    elif status_code == 630:
        print(f'Error {status_code}: Invalid operands')
    clientSocket.close()