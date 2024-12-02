import struct

class Packet:
    def __init__(self, sequence_num, flags, ack_num, payload, rwnd=0):
        self.sequence_num = sequence_num
        self.flags = flags
        self.ack_num = ack_num
        self.payload = payload
        self.rwnd = rwnd

    def change_to_bytes(self):
        header = struct.pack('IIIB', self.sequence_num, self.ack_num, self.rwnd, self.flags)
        payload_bytes = self.payload.encode()
        payload_length = len(payload_bytes)
        return header + struct.pack('I', payload_length) + payload_bytes

    def from_bytes_to(data):
        sequence_num, ack_num, rwnd, flags = struct.unpack('IIIB', data[:13])
        payload_length = struct.unpack('I', data[13:17])[0]
        payload = data[17:17 + payload_length].decode()
        return Packet(sequence_num, flags, ack_num, payload, rwnd)
    
    def __str__(self):

        syn_flag = bool(self.flags & 0b001)
        ack_flag = bool(self.flags & 0b010)
        fin_flag = bool(self.flags & 0b100)
        return (
            '------------------- start\n'
            f'Sequence number: {self.sequence_num}\n'
            f'Ack number: {self.ack_num}\n'
            f'SYN: {syn_flag}, ACK: {ack_flag}, FIN: {fin_flag}\n'
            f'Rwnd: {self.rwnd}\n'
            f'Payload\n--------\n{self.payload}\n'
            '------------------- end'
        )