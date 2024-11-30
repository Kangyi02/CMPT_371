from socket import *
from packet import Packet
import time

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverName = IPAddr
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_DGRAM)
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

nextseqnum = 0
seq = 0
clientSocket.settimeout(0.0) # non blocking

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
        clientSocket.sendto(packet.change_to_bytes(),(serverName, serverPort))
        
        print('length of sndpkt:', len(sndpkt))
        if len(sndpkt) == 1:
            set_timer = time.time()
            nextseqnum += len(data)

        data = f.read(50)


    # recv
    try: # actually recv somthing
        ack, serverAddress = clientSocket.recvfrom(2048)
        response_packet = Packet.from_bytes_to(ack)
        print(response_packet)
        print('wthin try block, received packs ack_num:', response_packet.ack_num, 'the ack that is excepted:', nextseqnum)
        if (response_packet.ack_num == nextseqnum): # checking if it the correct 
            print('correct packet')
            sndpkt.pop(0)
            set_timer = time.time()
            if len(sndpkt) > 0:
                nextseqnum += len(sndpkt[0].payload)
    except Exception as e: # didn't recv anything
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
            clientSocket.sendto(pkt.change_to_bytes(),(serverName, serverPort))
        set_timer = time.time()
        
    
