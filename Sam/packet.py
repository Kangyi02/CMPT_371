import struct

class Packet:
    def __init__(self, sequence_num, syn_flag, ack_flag, ack_num, payload):
        self.sequence_num = sequence_num
        self.syn_flag = syn_flag
        self.ack_num = ack_num
        self.ack_flag = ack_flag
        self.payload = payload

    def change_to_bytes(self):
        header = struct.pack('II??', self.sequence_num, self.ack_num, self.syn_flag, self.ack_flag)
        payload_bytes = self.payload.encode()
        payload_length = len(payload_bytes)
        return header + struct.pack('I', payload_length) + payload_bytes

    def from_bytes_to(data):
        sequence_num, ack_num, syn_flag, ack_flag = struct.unpack('II??', data[:10])
        payload_length = struct.unpack('I', data[10:14])[0]
        payload = data[14:14 + payload_length].decode()
        return Packet(sequence_num, syn_flag, ack_flag, ack_num, payload)
    
    def __str__(self):
        return str(self.sequence_num) + '\n' \
            + str(self.ack_num) + '\n' \
            + str(self.ack_flag) + str(self.syn_flag) +'\n' \
            + self.payload