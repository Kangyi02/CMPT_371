from socket import *
from packet import Packet
import time
import random

hostname = gethostname()
IPAddr = gethostbyname(hostname)

receiverName = IPAddr
receiverPort = 1200

senderSocket = socket(AF_INET, SOCK_DGRAM)
f  = open('test.txt')

ssthresh = float('INF')
cwnd = 1
dupAckCount = 0

# send packet
# set timer for correct ack number
# if recieve other ack start resending from that point.
# if recieve other ack 3 times in a row or time out reset cwnd to 1 
# when you recieve send two more packets


too_long = 2
sndpkt = []
ack_num = 1 # set from handshake

seq = 0
senderSocket.settimeout(0.01) # non blocking

data = f.read(50)
while data!='' or len(sndpkt) != 0: # data from above or data in queue
    time.sleep(1)
    # get data from above
    if data != '':
        
        print('reading more data\n', data)
        ack_num = ack_num + len(data)
        packet = Packet(seq, False, True, ack_num, data)
        seq += len(data)
        sndpkt.append(packet)
        senderSocket.sendto(packet.change_to_bytes(),(receiverName, receiverPort))
        
        print('length of sndpkt:', len(sndpkt))
        if len(sndpkt) == 1:
            set_timer = time.time()

        data = f.read(50)


    # recv
    try: # actually recv somthing
        ack, receiverAddress = senderSocket.recvfrom(2048)
        if random.random() > 0.25: # simulate packets being dropped on the way back
            response_packet = Packet.from_bytes_to(ack)
            print(response_packet)
            print('received packs ack_num:', response_packet.ack_num, 'the ack that is excepted:', sndpkt[0].sequence_num+1)
            for i, pkt in enumerate(sndpkt):
                if (response_packet.ack_num == pkt.sequence_num+1): # checking if it the correct 
                    print('correct packet')
                    sndpkt = sndpkt[i+1:]
                    set_timer = time.time()
                    break
    except TimeoutError as e: # didn't recv anything
        print(e)
        print('Nothing to recieve at socket')
        print('data> ->', data, '<- length of unAck packets:', len(sndpkt))
    
    # timeout
    if time.time() - set_timer > too_long:
        print('Timeout happened')
        print('how many packets ',len(sndpkt))
        for i, pkt in enumerate(sndpkt):
            print('sending the:', i)
            print(pkt.sequence_num)
            senderSocket.sendto(pkt.change_to_bytes(),(receiverName, receiverPort))
        set_timer = time.time()
        
    
