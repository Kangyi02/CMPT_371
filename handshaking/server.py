# server
from socket import *
from packet import * 

# create a udp socket connection
serverPort = 12002
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print ("The server is ready to hand shake")

is_client_alive = False

# the server received the TCP SYNACK from the client
message, clientAddress = serverSocket.recvfrom(2048)
received_packet = Packet.from_bytes_to(message)
print(received_packet.sequence_num)
print(received_packet.syn)

# create a SYNACK, then sends back to the client

# then the server receives the ACK from the client, done




while is_client_alive:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)