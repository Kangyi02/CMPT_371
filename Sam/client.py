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
# Packet gets set up by handshake, for now hard coded



data = f.read(50)
while data != '':
    packet = Packet(0, 1, True, data)
    length = clientSocket.sendto(packet.change_to_bytes(),(serverName, serverPort))
    print('length of message sent:', length, 'len of message:', len(data))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(Packet.from_bytes_to(modifiedMessage))
    data = f.read(50)


# send packet
# set timer for correct ack number
# if recieve other ack start resending from that point.
# if recieve other ack 3 times in a row or time out reset cwnd to 1 
# when you recieve send two more packets

too_long = 10
set_Timer = time.time()
savedPackets = {}

while data!='': # data from above
    currentlyAccepting = 0 # set from handshake
    
    #wrap data
    packet = Packet()
    set_Timer = time.time()
    
    if set_Timer - time.time() < too_long or currentlyAccepting:
        # time out stuff
        ssthresh = cwnd / 2


 