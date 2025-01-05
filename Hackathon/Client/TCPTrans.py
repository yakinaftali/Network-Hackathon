import socket
import time
import struct

from Hackathon.Client.Transfer import Transfer


class TCPTrans(Transfer):

    def __init__(self, ip, port, size):
        super().__init__(ip, port, size)
        self.socket = None

    def start(self):
        """Start the TCP transfer"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))

        # Send file size over the TCP connection (as string followed by a newline)
        self.socket.sendall(f"{self.file_size}\n".encode())

        # Start the transfer and measure time
        self.start_time = time.time()

        # Receive the file in chunks and accumulate it
        total_received = 0
        with open("received_file", "wb") as f:
            while total_received < self.file_size:
                data = self.socket.recv(1024)  # Receive in chunks of 1024 bytes
                if not data:
                    break  # If no data is received, exit the loop
                total_received += len(data)
                f.write(data)
                print(f"Received {total_received} bytes")

        total_time = time.time() - self.start_time
        self.log_transfer_details(total_time)

        # Close the socket after the transfer is complete
        self.socket.close()

    def log_transfer_details(self, total_time):
        """Logs the details of the transfer"""
        transfer_speed = (self.file_size * 8) / total_time  # Speed in bits per second
        print(
            f"TCP transfer finished, total time: {total_time:.2f} seconds, total speed: {transfer_speed:.2f} bits/second")
