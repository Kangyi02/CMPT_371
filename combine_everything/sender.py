from socket import *
from packet import Packet
import time
import random

hostname = gethostname()
IPAddr = gethostbyname(hostname)
receiverName = IPAddr
receiverPort = 1200

senderSocket = socket(AF_INET, SOCK_DGRAM)
f  = open('test.txt')

too_long = 2
sndpkt = []
# ack_num = 1 # set from handshake

prev_ack_num = -1

senderSocket.settimeout(0.01) # non blocking

# for congestion control, slow start
cwnd = 1
ssthresh = float('INF')
dupAckCount = 0 # Loss indicated by timeout: TCP tahoe

# flow control
rwnd = float('INF')



## handshake part
is_server_alive = False
initial_sequence_num = 0

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
            senderSocket.sendto(initial_packet.change_to_bytes(), (receiverName, receiverPort))

            # the client receives the SYNACK
            message, serverAddress = senderSocket.recvfrom(2048)
            received_packet = Packet.from_bytes_to(message)

            if received_packet.flags==0b110 and received_packet.ack_num==initial_packet.sequence_num+1:
                # sends back a ACK indicates it receives the SYNACK
                ack_num = received_packet.sequence_num+1
                #print(ack_num)
                receiver_ack_packet = Packet(0, 0b010, ack_num, '')

                # timer?
                senderSocket.sendto(receiver_ack_packet.change_to_bytes(), (receiverName, receiverPort))

                print ("The server is alive!")
                return True
            
        except socket.timeout:
            num_of_sends+=1
            print("Timeout, resending TCP SYN packet!")

    print("Handshake failed.")
    return False

is_server_alive = handshake_client_side()
##

next_seq_num = initial_sequence_num

if is_server_alive:
    data = f.read(50)
    while data!='' or len(sndpkt) != 0: # data from above or data in queue
        time.sleep(1)

        window_size = min(cwnd, rwnd)
        if window_size==rwnd:
            print("set window size to rwnd!!")

        # get data from above
        while data != '' and len(sndpkt)<window_size: # when unacked packets size is less than the window size
            
            print('reading more data\n', data)
            #ack_num = ack_num + len(data)
            packet = Packet(next_seq_num, 0b001, 0, data) # changed ack flag to false
            next_seq_num += len(data)
            sndpkt.append(packet)
            senderSocket.sendto(packet.change_to_bytes(),(receiverName, receiverPort))
            
            print('length of sndpkt:', len(sndpkt))

            if len(sndpkt) == 1:
                set_timer = time.time()

            data = f.read(50)

        # recv
        try: # actually recv somthing
            ack_packet, receiverAddress = senderSocket.recvfrom(2048)
            if random.random() > 0.25: # simulate packets being dropped on the way back
                response_packet = Packet.from_bytes_to(ack_packet)
                print(response_packet)
                print('received packs ack_num:', response_packet.ack_num, 'the ack that is excepted:', sndpkt[0].sequence_num+1)
                rwnd = response_packet.rwnd
                
                # if it is a dup ack, increase the counter
                if response_packet.ack_num == prev_ack_num:
                    dupAckCount+=1
                    print(f"dup ack count: {dupAckCount}")
                else: # if it is a new ack, reset the new ack counter
                    dupAckCount=0

                # TCP tahoe, 3 dup acks, reset the cwnd, resend pkts
                if dupAckCount==3:               
                    # retransimit
                    for i, pkt in enumerate(sndpkt):
                        print('sending the:', i)
                        print(pkt.sequence_num)
                        senderSocket.sendto(pkt.change_to_bytes(),(receiverName, receiverPort))
                    cwnd = 1
                    ssthresh = max(cwnd/2, 1)
                    dupAckCount = 0
                    set_timer = time.time()
                else: # pop out the acked packet
                    for i, pkt in enumerate(sndpkt):
                        if (response_packet.ack_num == pkt.sequence_num+1): # checking if it the correct 
                            print('correct packet')
                            sndpkt = sndpkt[i+1:] # pop out the acked packet
                            set_timer = time.time()
                            break
                
                prev_ack_num = response_packet.ack_num
            else:
                print("packet lost!")

            # congestion control 
            if cwnd<ssthresh: 
                cwnd *= 2
                print(f"slow start: cwnd double to {cwnd}")
            else:
                cwnd += 1 # congestion avoidance, linear increase
                print(f"congestion avoidance: cwnd linear to {cwnd}")

        except TimeoutError as e: # didn't recv anything
            print(e)
            print('Nothing to recieve at socket')
            print('data> ->', data, '<- length of unAck packets:', len(sndpkt))
        
        # timeout, retransmit all packets in the window
        if time.time() - set_timer > too_long:
            print('Timeout happened')
            print('how many packets ',len(sndpkt))
            for i, pkt in enumerate(sndpkt):
                print('sending the:', i)
                print(pkt.sequence_num)
                senderSocket.sendto(pkt.change_to_bytes(),(receiverName, receiverPort))

            ssthresh = max(cwnd/2, 1) # reduce the size
            cwnd = 1 # reset to slow start
            set_timer = time.time()
            
    
