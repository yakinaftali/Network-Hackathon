import socket
import time
import struct

from Hackathon.Server.Handler import Handler


class UDPHandler(Handler):
    def __init__(self, data, address, file_size, udp_socket):
        super().__init__(file_size)
        self.data = data
        self.address = address
        self.udp_socket = udp_socket

    def start_transfer(self):
        """Start sending file segments over UDP."""
        data_sent = 0
        sequence_number = 0
        while data_sent < self.file_size:
            segment = struct.pack('!QHQ', self.file_size, sequence_number, b'0')  # Packing size, seq, data
            self.udp_socket.sendto(segment, self.address)
            data_sent += len(segment)
            sequence_number += 1

        total_time = time.time() - self.start_time
        self.log_transfer_info("UDP", total_time)
