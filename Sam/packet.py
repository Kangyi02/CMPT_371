import struct

class Packet:
    def __init__(self, sequence_num, syn, ack, payload):
        self.sequence_num = sequence_num
        self.syn = syn
        self.ack = ack
        self.payload = payload

    def change_to_bytes(self):
        header = struct.pack('III', self.sequence_num, self.syn, self.ack)
        payload_bytes = self.payload.encode()
        payload_length = len(payload_bytes)
        return header + struct.pack('I', payload_length) + payload_bytes

    def from_bytes_to(data):
        sequence_num, syn, ack = struct.unpack('III', data[:12])
        payload_length = struct.unpack('I', data[12:16])[0]
        payload = data[16:16 + payload_length].decode()
        return Packet(sequence_num, syn, ack, payload)
    
    def __str__(self):
        return self.payload