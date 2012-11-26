HashCollisioneer
================

checks a predefined list of names and hash-functions for hash collisions to find the best suiting hash for some sample data


Implemented HashFunctions:

1. ELFHash0x10000
2. ELFHash0xffff
3. crc16str
4. crc16
5. crc16netsnmp9rounds
5. crc16netsnmp8rounds


Purpose
---------

originally designed to find collisions in short hash-algorithms for use with linux network device names (eth%d,port%d,..)
At the moment the script checks which one of the listed hash-algorithms is best for hashing devicenames like eth0-eth128, port0-port128,...
