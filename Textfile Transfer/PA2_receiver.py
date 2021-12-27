#!/usr/bin/env python3
# Last updated: Oct, 2021

import sys
import time
from socket import *
# import socket
import datetime 
from checksum import checksum, checksum_verifier

CONNECTION_TIMEOUT = 60 # timeout when the receiver cannot find the sender within 60 seconds
FIRST_NAME = "CHRISTOPHER"
LAST_NAME = "TRAN"

def start_receiver(server_ip, server_port, connection_ID, loss_rate=0.0, corrupt_rate=0.0, max_delay=0.0):
    """
     This function runs the receiver, connnect to the server, and receiver file from the sender.
     The function will print the checksum of the received file at the end. 
     The checksum is expected to be the same as the checksum that the sender prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running receiver: {}".format(datetime.datetime.now()))

    checksum_val = "00000"

    ##### START YOUR IMPLEMENTATION HERE #####

    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP type
    try: 
        clientSocket.settimeout(CONNECTION_TIMEOUT)
        clientSocket.connect((server_ip, server_port))
    except timeout:
        print(f'ERROR COULD NOT CONNECT TO ({server_ip}, {server_port})')
        sys.exit()

    text = ""
    send_ack = 0
    last_msg = "  1                      "
    last_msg = f'{last_msg}{checksum(last_msg)}'

    # set up with server_ip
    msg = f'HELLO R {loss_rate} {corrupt_rate} {max_delay} {connection_ID}'
    clientSocket.send(msg.encode("utf-8"))
    # waiting for "OK" or "ERROR"
    reply = "WAITING"
    while reply == "WAITING":
        reply = clientSocket.recv(1024).decode("utf-8")
    print(reply)
    try:
        while True:
            reply = clientSocket.recv(1024).decode("utf-8")
            recv_ack = int(reply[0])
            payload = reply[4:24]
            #recv_seq, recv_ack, payload, recv_checksum = reply[parts]
            # checks if given checksum matches reply
            if not checksum_verifier(reply[0:30]):
                clientSocket.send(last_msg.encode("utf-8"))
                continue
            # checks if correct expected ack received
            if recv_ack != send_ack:
                clientSocket.send(last_msg.encode("utf-8"))
                continue
            # save the payload!
            text = f'{text}{payload}'
            checksum_val = checksum(text)
            # reply with ack
            msg = f'  {send_ack}                      '
            msg = f'{msg}{checksum(msg)}'
            clientSocket.send(msg.encode("utf-8"))
            # update trackers
            send_ack = (send_ack + 1) % 2
            last_msg = msg
            # when client socket closes, gaia automatically closes this socket too
    except:
        # print("server_ip closed its socket")
        clientSocket.close()
        pass

    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running receiver: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))

    return checksum_val

 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 7:
        print("Expected \"python PA2_receiver.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay>\"")
        exit()
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay = sys.argv[1:]
    # START RECEIVER
    start_receiver(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay)
