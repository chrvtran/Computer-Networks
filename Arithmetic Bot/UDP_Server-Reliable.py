from socket import *
import sys

OK = '200'
# custom 600-799
INVALID_OC = '620'
INVALID_OPERAND = '630'

serverPort = 50001
serverSocket = socket(AF_INET, SOCK_DGRAM) # UDP type
serverSocket.bind(('', serverPort))
#print('Server is ready to receive') # remove when submitting

try:
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        # format message and check validity
        result = -1
        message = message.decode().rstrip()
        message_ops = message.split()
        if len(message_ops) != 3:
            # not correct format, return error
            print(f'{message} -> {INVALID_OC} {result}')
            buffer = f'{INVALID_OC} {result}'
            serverSocket.sendto(buffer.encode(), clientAddress)
            continue

        op = message_ops[0]
        int1 = None
        int2 = None
        if message_ops[1].lstrip('-').isdigit() and message_ops[2].lstrip('-').isdigit():
            int1 = int(message_ops[1])
            int2 = int(message_ops[2])
        else:
            # missing 1 or 2 integers, return error
            print(f'{message} -> {INVALID_OPERAND} {result}')
            buffer = f'{INVALID_OPERAND} {result}'
            serverSocket.sendto(buffer.encode(), clientAddress)
            continue
        
        # begin checking for op and solving problem
        if op == '+':
            result = int1 + int2
        elif op == '-':
            result = int1 - int2
        elif op == '*':
            result = int1 * int2
        elif op == '/':
            if int2 == 0:
                print(f'{message} -> {INVALID_OPERAND} {result}')
                buffer = f'{INVALID_OPERAND} {result}'
                serverSocket.sendto(buffer.encode(), clientAddress)
                continue
            result = int1 / int2
        else:
            # unknown op, return error
            print(f'{message} -> {INVALID_OC} {result}')
            buffer = f'{INVALID_OC} {result}'
            serverSocket.sendto(buffer.encode(), clientAddress)
            continue
        
        # all set to send results back to client
        print(f'{message} -> {OK} {result}')
        buffer = f'{OK} {result}'
        # server address automatically attached
        serverSocket.sendto(buffer.encode(), clientAddress)

except KeyboardInterrupt:
    serverSocket.close()
    sys.exit()
