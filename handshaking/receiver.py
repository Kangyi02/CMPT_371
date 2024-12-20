# server
from socket import *
from packet import * 

# create a udp socket connection
serverPort = 12013
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
serverSocket.settimeout(200)

is_client_alive = False
initial_seq_num = 10000

def handshake_server_side():
    print ("The server is ready to hand shake")
    # sequence_num, syn_flag, ack_flag, ack_num, payload
    # the server received the TCP SYNACK from the client
    message, clientAddress = serverSocket.recvfrom(2048)
    received_packet = Packet.from_bytes_to(message)

    # create a SYNACK, then sends back to the client
    if received_packet.flags == 0b100:
        ack_num = received_packet.sequence_num + 1
        print("The initial sequence number from receiver is: ", initial_seq_num)
        sender_ack_syn_packet = Packet(initial_seq_num, 0b110, ack_num, '')
        print("The SYN flag is true, receiver starts to establish connection")
        print("The ACK number for SYN message is: ", ack_num)
        # timer
        num_of_sends = 1
        max_num_of_sends = 4

        while num_of_sends<=max_num_of_sends:
            try:
                serverSocket.sendto(sender_ack_syn_packet.change_to_bytes(), clientAddress)

                message, clientAddress = serverSocket.recvfrom(2048)
                received_packet = Packet.from_bytes_to(message)
                # print(received_packet.ack_num)

                # then the server receives the ACK from the client, done
                if received_packet.flags==0b010 and received_packet.ack_num==sender_ack_syn_packet.sequence_num+1:
                    print("The ACK flag is true, received ACK\n")
                    print("The received ACK number is: ", received_packet.ack_num)
                    print ("The client is alive!")
                    return True
                
            except socket.timeout:
                num_of_sends+=1
                print("Timeout, resending TCP SYNACK packet!")

    return False

is_client_alive = handshake_server_side()

while is_client_alive:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)