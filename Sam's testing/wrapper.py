class wrapper:
    def __init__(self, source_port, dest_port, seq_num = 0, ack_num = 0, receive_window=512) -> None:
        self.source_port = source_port
        self.dest_port = dest_port
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.receive_window = receive_window
        
    def __str__(self):
        return self.source_port + ' ' + self.dest_port + ' ' + self.seq_num + ' ' + self.ack_num + ' ' + self.receive_window
