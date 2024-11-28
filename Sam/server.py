from socket import *
from packet import Packet
import random

serverPort = 1200
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(20)
nextseqnum = 0 # set by hand shake
sndpkt = Packet(0, False, True, nextseqnum, 'empty')
print ('The server is ready to receive')
flag = True
while flag:
    try:
        message, clientAddress = serverSocket.recvfrom(2048)
    except:
        flag = False
        print('timeout server closing')
    packet = Packet.from_bytes_to(message)
    
    if random.random() > 0.25: # pretend to receive packet
        print(packet)
        if nextseqnum == packet.sequence_num: 
            # if it is he next packet respond with the correct ack
            # else respond with the previous ack and keep doing that 
            # until the right packet is sent
            print('correct packet')
            nextseqnum = packet.sequence_num + len(packet.payload)
            payload = packet.payload
            sndpkt = Packet(0, False, True, nextseqnum, packet.payload.upper())
        else:
            print('incorrect packet, sending expected')
        serverSocket.sendto(sndpkt.change_to_bytes(),clientAddress)
    