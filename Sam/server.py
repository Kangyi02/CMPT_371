from socket import *
from packet import Packet

serverPort = 1200
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    packet = Packet.from_bytes_to(message)

    packet.payload = packet.payload.upper()
    serverSocket.sendto(packet.change_to_bytes(),clientAddress)