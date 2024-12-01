from socket import *
from packet import Packet
import random

receiverPort = 1200
receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
receiverSocket.settimeout(20)
nextseqnum = 0 # set by hand shake
sndpkt = Packet(0, False, True, nextseqnum, 'empty')
print ('Receiver is ready to receive')
flag = True
while flag:
    try:
        message, senderAddress = receiverSocket.recvfrom(2048)
    except:
        print('timeout receiver closing')
        break
    packet = Packet.from_bytes_to(message)
    
    if random.random() > 0.25: # pretend to receive packet
        print(packet)
        if nextseqnum == packet.sequence_num: 
            # if it is he next packet respond with the correct ack
            # else respond with the previous ack and keep doing that 
            # until the right packet is sent
            
            
            payload = packet.payload
            sndpkt = Packet(0, False, True, nextseqnum+1, packet.payload.upper())
            print('correct packet sending response with ack number:', nextseqnum+1)
            nextseqnum += len(packet.payload)
        else:
            print('incorrect packet, sending expected')
        receiverSocket.sendto(sndpkt.change_to_bytes(),senderAddress)
    