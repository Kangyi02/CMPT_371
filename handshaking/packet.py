import struct

# 0b000
# syn, ack, fin
class Packet:
    #def __init__(self, sequence_num, syn_flag, ack_flag, ack_num, payload):
    def __init__(self, sequence_num, flags, ack_num, payload):
        self.sequence_num = sequence_num
        #self.syn_flag = syn_flag
        self.flags = flags
        self.ack_num = ack_num
        #self.ack_flag = ack_flag
        self.payload = payload

    def change_to_bytes(self):
        # header = struct.pack('II??', self.sequence_num, self.ack_num, self.syn_flag, self.ack_flag)
        header = struct.pack('IIB', self.sequence_num, self.ack_num, self.flags)
        payload_bytes = self.payload.encode()
        payload_length = len(payload_bytes)
        return header + struct.pack('I', payload_length) + payload_bytes

    def from_bytes_to(data):
        sequence_num, ack_num, flags = struct.unpack('IIB', data[:9])
        payload_length = struct.unpack('I', data[9:13])[0]
        payload = data[13:13 + payload_length].decode()
        return Packet(sequence_num, flags, ack_num, payload)