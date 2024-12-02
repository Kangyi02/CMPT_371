import struct

class Packet:
    def __init__(self, sequence_num, syn_flag, ack_flag, ack_num, payload, rwnd=0):
        self.sequence_num = sequence_num
        self.syn_flag = syn_flag
        self.ack_num = ack_num
        self.ack_flag = ack_flag
        self.payload = payload
        self.rwnd = rwnd

    def change_to_bytes(self):
        header = struct.pack('II??I', self.sequence_num, self.ack_num, self.syn_flag, self.ack_flag, self.rwnd)
        payload_bytes = self.payload.encode()
        payload_length = len(payload_bytes)
        return header + struct.pack('I', payload_length) + payload_bytes

    def from_bytes_to(data):
        sequence_num, ack_num, syn_flag, ack_flag, rwnd = struct.unpack('II??I', data[:16])
        payload_length = struct.unpack('I', data[16:20])[0]
        payload = data[20:20 + payload_length].decode()
        return Packet(sequence_num, syn_flag, ack_flag, ack_num, payload, rwnd)
    
    def __str__(self):
        return '------------------- start\n'+ 'Sqeunce number: ' \
            + str(self.sequence_num) + '\n' \
            + 'Ack number: '+ str(self.ack_num) + '\n' \
            + 'Ack Flag: ' + str(self.ack_flag) \
            + '  SYN flag: ' + str(self.syn_flag) +'\n' \
            + 'Payload\n--------\n' +self.payload \
            + '\n------------------- end'