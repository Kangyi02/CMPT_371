from socket import *
from packet import Packet
import random

receiverPort = 1200
receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
receiverSocket.settimeout(20)


# hand shake part
is_client_alive = False
initial_seq_num = 0

def handshake_server_side():
    print ("The server is ready to hand shake")
    # sequence_num, syn_flag, ack_flag, ack_num, payload
    # the server received the TCP SYNACK from the client
    message, clientAddress = receiverSocket.recvfrom(2048)
    print(clientAddress)
    received_packet = Packet.from_bytes_to(message)

    # create a SYNACK, then sends back to the client
    if received_packet.flags == 0b100:
        ack_num = received_packet.sequence_num + 1
        sender_ack_syn_packet = Packet(initial_seq_num, 0b110, ack_num, '')

        # timer
        num_of_sends = 1
        max_num_of_sends = 4

        while num_of_sends<=max_num_of_sends:
            try:
                receiverSocket.sendto(sender_ack_syn_packet.change_to_bytes(), clientAddress)

                message, clientAddress = receiverSocket.recvfrom(2048)
                received_packet = Packet.from_bytes_to(message)
                # print(received_packet.ack_num)

                # then the server receives the ACK from the client, done
                if received_packet.flags==0b010 and received_packet.ack_num==sender_ack_syn_packet.sequence_num+1:
                    print ("The client is alive!")
                    return True
                
            except socket.timeout:
                num_of_sends+=1
                print("Timeout, resending TCP SYNACK packet!")

    return False

is_client_alive = handshake_server_side()
##


if is_client_alive:
    nextseqnum = 0 # set by hand shake
    sndpkt = Packet(0, 0b010, nextseqnum, 'empty')
    print ('Receiver is ready to receive')
    last_ack_num = -1

    # flow control
    buffer_size = 1024
    buffer_used = 0

    flag = True
    while flag:
        try:
            message, senderAddress = receiverSocket.recvfrom(2048)
        except:
            print('timeout receiver closing')
            break

        packet = Packet.from_bytes_to(message)
        
        if random.random() > 0.1: # pretend to receive packet
            print(packet)

            # check if there is enough buffer
            if buffer_used+len(packet.payload)<=buffer_size:
                if nextseqnum == packet.sequence_num: 
                    # if it is he next packet respond with the correct ack
                    # else respond with the previous ack and keep doing that 
                    # until the right packet is sent        
                    payload = packet.payload
                    sndpkt = Packet(0, 0b010, nextseqnum+1, packet.payload.upper())
                    print('correct packet sending response with ack number:', nextseqnum+1)
                    nextseqnum += len(packet.payload)
                    last_ack_num = packet.sequence_num+1
                    print('latest ack number:', last_ack_num)
                else:
                    print('incorrect packet, resending last ack')
                    sndpkt = Packet(0, 0b010, last_ack_num, 'empty')
                    print('resent ack number:', sndpkt.ack_num)
            else:
                print("buffer full")
                sndpkt = Packet(0, 0b010, last_ack_num, 'empty')
            sndpkt.rwnd = buffer_size-buffer_used
            print('advertised rwnd:', sndpkt.rwnd)
            receiverSocket.sendto(sndpkt.change_to_bytes(),senderAddress)
        else:
            print('simulating packet loss')
    