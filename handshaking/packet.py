import struct

class Packet:
    def __init__(self, sequence_num, syn, ack, payload):
        self.sequence_num = sequence_num
        self.syn = syn
        self.ack = ack
        self.payload = payload

    def change_to_bytes(self):
        header = struct.pack('II?', self.sequence_num, self.ack, self.syn)
        payload_bytes = self.payload.encode()
        payload_length = len(payload_bytes)
        return header + struct.pack('I', payload_length) + payload_bytes

    def from_bytes_to(data):
        sequence_num, ack, syn = struct.unpack('II?', data[:9])
        payload_length = struct.unpack('I', data[9:13])[0]
        payload = data[13:13 + payload_length].decode()
        return Packet(sequence_num, syn, ack, payload)