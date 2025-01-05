import socket
import time

from Hackathon.Server.Handler import Handler


class TCPHandler(Handler):
    def __init__(self, connection, file_size):
        super().__init__(file_size)
        self.connection = connection

    def start(self):
        """Start sending the file over TCP."""
        data_sent = 0
        while data_sent < self.file_size:
            self.connection.sendall(b'0')  # Sending 1 byte at a time (for simplicity)
            data_sent += 1

        total_time = time.time() - self.start_time
        self.connection.close()

        self.log_transfer_info("TCP", total_time)
