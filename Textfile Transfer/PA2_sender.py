#!/usr/bin/env python3
# Last updated: Oct, 2021

import sys
from socket import *
# import socket
import datetime
from checksum import checksum, checksum_verifier

CONNECTION_TIMEOUT = 60 # timeout when the sender cannot find the receiver within 60 seconds
FIRST_NAME = "CHRISTOPHER"
LAST_NAME = "TRAN"

MAXTRANSFERRED = 200
MAXREAD = 20

def start_sender(server_ip, server_port, connection_ID, loss_rate=0, corrupt_rate=0, max_delay=0, transmission_timeout=60, filename="declaration.txt"):
    """
     This function runs the sender, connnect to the server, and send a file to the receiver.
     The function will print the checksum, number of packet sent/recv/corrupt recv/timeout at the end. 
     The checksum is expected to be the same as the checksum that the receiver prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)
        tranmission_timeout - waiting time until the sender resends the packet again (int - default is 60 seconds and cannot be 0)
        filename - the path + filename to send (String)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
        total_packet_sent - the total number of packet sent (int)
        total_packet_recv - the total number of packet received, including corrupted (int)
        total_corrupted_pkt_recv - the total number of corrupted packet receieved (int)
        total_timeout - the total number of timeout (int)

    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running sender: {}".format(datetime.datetime.now()))

    checksum_val = "00000"
    total_packet_sent = 0
    total_packet_recv = 0
    total_corrupted_pkt_recv = 0
    total_timeout =  0

    print("Connecting to server: {}, {}, {}".format(server_ip, server_port, connection_ID))

    ##### START YOUR IMPLEMENTATION HERE #####

    # partition text file into MAXREAD bytes up to MAXTRANSFERRED
    lines = []
    with open(filename) as file:
        text = file.read(MAXTRANSFERRED)
        checksum_val = checksum(text)
        for i in range(0, MAXTRANSFERRED, MAXREAD):
            lines.append(text[i:i+MAXREAD])

    # create 1 TCP connection
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.settimeout(CONNECTION_TIMEOUT)
        clientSocket.connect((server_ip, server_port))
    except:
        print(f'ERROR COULD NOT CONNECT TO ({server_ip}, {server_port})')
        sys.exit()

    # set up with server_ip
    msg = f'HELLO S {loss_rate} {corrupt_rate} {max_delay} {connection_ID}'
    clientSocket.send(msg.encode("utf-8"))
    # waiting for "OK" or "ERROR"
    reply = "WAITING"
    while reply == "WAITING":
       reply = clientSocket.recv(1024).decode("utf-8")
    print(reply)
    # begin sending payload
    send_seq = 0
    for line in lines:
        redo = True
        reply = None
        msg = f'{send_seq} {(send_seq+1)%2} {"{:<20}".format(line)} '
        msg = f'{msg}{checksum(msg)}'
        while redo:
            try:
                redo = False
                # send msg and wait for reply
                total_packet_sent += 1
                clientSocket.send(msg.encode("utf-8"))
                clientSocket.settimeout(transmission_timeout)
                while True:
                    reply = clientSocket.recv(1024).decode("utf-8")
                    total_packet_recv += 1
                    # checks corruption, if corrupt wait it out
                    if not checksum_verifier(reply[0:30]):
                        total_corrupted_pkt_recv += 1
                        continue
                    # if packet is not corrupt but has wrong ack
                    # recv until timeout (might be a delayed packet)
                    recv_ack = int(reply[2])
                    if recv_ack != send_seq:
                        continue
                    # otherwise, send next payload
                    break
            except timeout:
                # send again if timeout
                total_timeout += 1
                redo = True
                continue
        send_seq = (send_seq + 1) % 2
        # transfer of 20 bytes is successful!

    # file transfered completely
    clientSocket.close()

    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running sender: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))
    print("Total packet sent: {}".format(total_packet_sent))
    print("Total packet recv: {}".format(total_packet_recv))
    print("Total corrupted packet recv: {}".format(total_corrupted_pkt_recv))
    print("Total timeout: {}".format(total_timeout))

    return (checksum_val, total_packet_sent, total_packet_recv, total_corrupted_pkt_recv, total_timeout)
 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 9:
        print("Expected \"python3 PA2_sender.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay> <transmission_timeout> <filename>\"")
        exit()

    # ASSIGN ARGUMENTS TO VARIABLES
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay, transmission_timeout, filename = sys.argv[1:]
    
    # RUN SENDER
    start_sender(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay, float(transmission_timeout), filename)
