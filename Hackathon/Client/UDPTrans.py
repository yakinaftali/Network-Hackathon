import socket
import time

from Hackathon.Client.Transfer import Transfer


class UDPTrans(Transfer):

    def __init__(self, ip, port, size):
        super().__init__(ip, port, size)
        self.socket = None

    def start(self):
        """Start the UDP transfer"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send a request packet (requesting file size)
        self.socket.sendto(f"{self.file_size}\n".encode(), (self.server_ip, self.server_port))

        # Start measuring time
        self.start_time = time.time()

        total_received = 0
        while total_received < self.file_size:
            # Receive the payload (data segments) from the server
            data, _ = self.socket.recvfrom(1024)
            total_received += len(data)

        total_time = time.time() - self.start_time
        self.log_transfer_details(total_time)
        self.socket.close()

