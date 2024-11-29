from socket import *
from packet import * 

# create a udp socket connection
serverName = gethostname()
serverPort = 12019
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2)

# global variable to see if hand shake successful
is_server_alive = False
initial_sequence_num = 12345

# 0b000
# syn, ack, fin

def handshake_client_side():
    print ("The client is ready to hand shake")

    #order: sequence_num, syn_flag, ack_flag, ack_num, payload
    # the client makes a packet, set SYN flag to true 
    initial_packet = Packet(initial_sequence_num, 0b100, 0, '')

    # the client sends a packet including the TCP SYN msg
    # timer
    num_of_sends = 1
    max_num_of_sends = 4

    while num_of_sends<=max_num_of_sends:
        try:
            clientSocket.sendto(initial_packet.change_to_bytes(), (serverName, serverPort))

            # the client receives the SYNACK
            message, serverAddress = clientSocket.recvfrom(2048)
            received_packet = Packet.from_bytes_to(message)

            if received_packet.flags==0b110 and received_packet.ack_num==initial_packet.sequence_num+1:
                # sends back a ACK indicates it receives the SYNACK
                ack_num = received_packet.sequence_num+1
                #print(ack_num)
                receiver_ack_packet = Packet(0, 0b010, ack_num, '')

                # timer?
                clientSocket.sendto(receiver_ack_packet.change_to_bytes(), (serverName, serverPort))

                print ("The server is alive!")
                return True
            
        except socket.timeout:
            num_of_sends+=1
            print("Timeout, resending TCP SYN packet!")

    print("Handshake failed.")
    return False

is_server_alive = handshake_client_side()
while is_server_alive:
    message = input('Input lowercase sentence:')
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())

clientSocket.close()