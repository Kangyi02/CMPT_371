# server
from socket import *
from packet import * 

# create a udp socket connection
serverPort = 12012
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

is_client_alive = False
initial_seq_num = 20000

def handshake_server_side():
    print ("The server is ready to hand shake")
    # sequence_num, syn_flag, ack_flag, ack_num, payload
    # the server received the TCP SYNACK from the client
    message, clientAddress = serverSocket.recvfrom(2048)
    received_packet = Packet.from_bytes_to(message)

    # create a SYNACK, then sends back to the client
    if received_packet.syn_flag:
        ack_num = received_packet.sequence_num + 1
        sender_ack_syn_packet = Packet(initial_seq_num, True, True, ack_num, '')

        serverSocket.sendto(sender_ack_syn_packet.change_to_bytes(), clientAddress)

        message, clientAddress = serverSocket.recvfrom(2048)
        received_packet = Packet.from_bytes_to(message)
        # print(received_packet.ack_num)

        # then the server receives the ACK from the client, done
        if received_packet.ack_flag and received_packet.ack_num==sender_ack_syn_packet.sequence_num+1:
            print ("The client is alive!")
            return True
        
    return False

is_client_alive = handshake_server_side()
while is_client_alive:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)