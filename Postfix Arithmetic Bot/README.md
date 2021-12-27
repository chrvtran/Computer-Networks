# Postfix Arithmetic Bot
Transport Layer Protocols: TCP, unreliable and reliable UDP

Notes: '127.0.0.1' is localhost, acceptable port numbers 1024-65535 inclusive

- socket Library used for creating and connecting sockets
- random Library used for seeding drop pattern based on drop probability
- sender sending one operation postfix expressions 1 line at a time
- receiver receives postfix and returns answer with 'OK' or error code with message

Command Lines
- python <reliable_server_filename>
- python <unreliable_server_filename> <drop_prob=[0.0 1.0]> <seed>
- python <any_client_filename> <txtfile>
