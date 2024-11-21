from socket import *
from packet import Packet
import random

serverPort = 1200
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(20)
print ('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    packet = Packet.from_bytes_to(message)
    if random.random() > 0.25:
        packet.payload = packet.payload.upper()
        serverSocket.sendto(packet.change_to_bytes(),clientAddress)