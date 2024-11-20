from socket import *
from packet import * 

# create a udp socket connection
serverName = gethostname()
serverPort = 12002
clientSocket = socket(AF_INET, SOCK_DGRAM)

# global variable to see if hand shake successful
is_server_alive = False
initial_sequence_num = 12345
SYN = 1
#order: sequence_num, syn, ack, payload

# the client makes a packet ??
intial_packet = Packet(initial_sequence_num, 1, 0, '')


# the client sends a packet incluing the TCP SYN msg
#clientSocket.sendto((str(initial_sequence_num) + str(SYN)).encode(), (serverName, serverPort))
clientSocket.sendto(intial_packet.change_to_bytes(), (serverName, serverPort))

# the client receives the SYNACK, sends back a ACK indicates it receives the SYNACK

while is_server_alive:
    message = input('Input lowercase sentence:')
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    clientSocket.close()