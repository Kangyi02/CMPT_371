from socket import *
from packet import Packet
import random

receiverPort = 1207
receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
receiverSocket.settimeout(50)

nextseqnum = 0 # set by hand shake
sndpkt = Packet(0, False, True, nextseqnum, 'empty')
print ('Receiver is ready to receive')
last_ack_num = -1

# flow control
buffer_size = 1024
buffer_used = 0

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

        # check if there is enough buffer
        if buffer_used+len(packet.payload)<=buffer_size:
            if nextseqnum == packet.sequence_num: 
                # if it is he next packet respond with the correct ack
                # else respond with the previous ack and keep doing that 
                # until the right packet is sent        
                payload = packet.payload
                sndpkt = Packet(0, False, True, nextseqnum+1, packet.payload.upper())
                print('correct packet sending response with ack number:', nextseqnum+1)
                nextseqnum += len(packet.payload)
                last_ack_num = packet.sequence_num+1
                print('latest ack number:', last_ack_num)
            else:
                print('incorrect packet, resending last ack')
                sndpkt = Packet(0, False, True, last_ack_num, 'empty')
                print('resent ack number:', sndpkt.ack_num)
        else:
            print("buffer full")
            sndpkt = Packet(0, False, True, last_ack_num, 'empty')
        sndpkt.rwnd = buffer_size-buffer_used
        print('advertised rwnd:', sndpkt.rwnd)
        receiverSocket.sendto(sndpkt.change_to_bytes(),senderAddress)
    else:
        print('simulating packet loss')
    