# File Transfer
Transport Protocol: TCP

Notes: transfers up to MAXTRANSFERRED bytes in segments of MAXREAD bytes

- socket Library used for creating and connecting sockets
- sender sends MAXREAD number of bytes parsed from a text file and sequence number
- there is a set chance of loss, corruption, and a fixed max delay
- receiver checks checksum and returns proper acknowledgement number accounting for any issues

Command Lines

- python PA2_sender.py <IP=gaia.cs.umass.edu> <port=20000> <4-digitID> <loss_rate=[0.0,1.0]> <corr_rate=[0.0,1.0]> <max_delay=[0,5]> <trans_timeout=60> <txtfile>
- python PA2_receiver.py <IP=gaia.cs.umass.edu> <port=20000> <4-digitID> <loss_rate=[0.0,1.0]> <corr_rate=[0.0,1.0]> <max_delay=[0,5]>