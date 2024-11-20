from socket import *
from wrapper import wrapper

hostname = gethostname()
IPAddr = gethostbyname(hostname)

serverName = IPAddr
serverPort = 1200

clientSocket = socket(AF_INET, SOCK_DGRAM)
f  = open('test.txt')


# wrapper gets set up by handshake, for now hard coded

header = wrapper()

data = f.read(500)
while data != '':
    length = clientSocket.sendto(data.encode(),(serverName, serverPort))
    print('length of message sent:', length, 'len of message:', len(data))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    data = f.read(500)