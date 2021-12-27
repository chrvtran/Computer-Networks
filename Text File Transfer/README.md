# Textfile Transfer
Transport Protocol: TCP

Notes: transfers up to MAXTRANSFERRED bytes in segments of MAXREAD bytes

- socket Library used for creating and connecting sockets
- sender sends proper sequence number and MAXREAD bytes parsed from a textfile
- there is a parameter set chance of loss, corruption, and max delay
- receiver checks checksum and returns proper ACK accounting for any issues, stores textfile accumulatively

Command Lines

- python PA2_sender.py <IP=gaia.cs.umass.edu> <port=20000> <4-digitID> <loss_rate=[0.0,1.0]> <corr_rate=[0.0,1.0]> <max_delay=[0,5]> <trans_timeout=60> <textfile>
- python PA2_receiver.py <IP=gaia.cs.umass.edu> <port=20000> <4-digitID> <loss_rate=[0.0,1.0]> <corr_rate=[0.0,1.0]> <max_delay=[0,5]>
