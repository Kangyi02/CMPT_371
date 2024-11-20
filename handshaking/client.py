from socket import *
from packet import * 

# create a udp socket connection
serverName = gethostname()
serverPort = 12012
clientSocket = socket(AF_INET, SOCK_DGRAM)

# global variable to see if hand shake successful
is_server_alive = False
initial_sequence_num = 12345

def handshake_client_side():
    print ("The client is ready to hand shake")

    #order: sequence_num, syn_flag, ack_flag, ack_num, payload
    # the client makes a packet, set SYN flag to true 
    intial_packet = Packet(initial_sequence_num, True, False, 0, '')

    # the client sends a packet including the TCP SYN msg
    clientSocket.sendto(intial_packet.change_to_bytes(), (serverName, serverPort))

    # the client receives the SYNACK
    message, serverAddress = clientSocket.recvfrom(2048)
    received_packet = Packet.from_bytes_to(message)

    if received_packet.ack_flag and received_packet.syn_flag and received_packet.ack_num==intial_packet.sequence_num+1:
        # sends back a ACK indicates it receives the SYNACK
        ack_num = received_packet.sequence_num+1
        #print(ack_num)
        receiver_ack_packet = Packet(0, False, True, ack_num, '')
        clientSocket.sendto(receiver_ack_packet.change_to_bytes(), (serverName, serverPort))

        print ("The server is alive!")
        return True
    
    return False

is_server_alive = handshake_client_side()
while is_server_alive:
    message = input('Input lowercase sentence:')
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())

clientSocket.close()