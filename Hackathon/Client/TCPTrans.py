import socket
import time

from Hackathon.Client.Transfer import Transfer


class TCPTrans(Transfer):

    def __init__(self, ip, port, size):
        super().__init__(ip, port,size)
        self.socket = None

    def start(self):
        """Start the TCP transfer"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

        # Send file size over the TCP connection
        self.socket.sendall(f"{self.file_size}\n".encode())

        # Start the transfer and measure time
        self.start_time = time.time()
        self.socket.recv(self.file_size)  # Receiving the file in chunks (to be implemented)

        total_time = time.time() - self.start_time
        self.log_transfer_details(total_time)
        self.socket.close()


