from socket import *
from packet import Packet

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverName = IPAddr
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_DGRAM)
f  = open('test.txt')

ssthresh = float('INF')
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
    # if recieve other ack or time out start resending from that point. and set 
    # when you recieve send two more packets
 