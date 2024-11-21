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
set_Timer = time.time()
savedPackets = {}
currentlyAccepting = 1 # set from handshake
seq_num = 0
clientSocket.settimeout(too_long)

data = f.read(50)
while data!='': # data from above
    currentlyAccepting = seq_num + len(data)
    # wrap data
    packet = Packet(seq_num, False, True, currentlyAccepting, data)
    seq_num += len(data)
    flag = True
    while flag:
        clientSocket.sendto(packet.change_to_bytes(),(serverName, serverPort))
        
        try:
            ack, serverAddress = clientSocket.recvfrom(2048)
            response_packet = Packet.from_bytes_to(ack)
            if (response_packet.ack_num == currentlyAccepting):
                flag = not flag
                print(response_packet.payload, response_packet.sequence_num)
        except:
            # timeout
            print('timeout happened, resending the sequence number:', packet.sequence_num)
            flag = False
        
    data = f.read(50)
