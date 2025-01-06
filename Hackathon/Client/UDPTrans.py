import socket
import time
import struct
from Hackathon.Client.Transfer import Transfer


class UDPTrans(Transfer):

    def __init__(self, ip, port, size):
        super().__init__(ip, port, size)
        self.socket = None
        self.received_segments = set()  # Set to track received segments

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

            # Parse the received packet (validate magic cookie and extract data)
            payload = self.parse_payload(data)
            if payload:
                segment_number, total_segments, segment_data = payload
                total_received += len(segment_data)

                # Track the received segment
                self.received_segments.add(segment_number)

                print(f"Received segment {segment_number}/{total_segments}")

                # If all segments are received, break the loop
                if len(self.received_segments) == total_segments:
                    print("All segments received, transfer complete.")
                    break

        total_time = time.time() - self.start_time
        self.log_transfer_details(total_time)

        self.socket.close()

    def parse_payload(self, message):
        """Parse the incoming UDP payload message"""
        try:
            # Check for magic cookie
            magic_cookie = message[:4]
            if magic_cookie != b'\xab\xcd\xdc\xba':  # Check for the expected magic cookie
                print("Invalid magic cookie in payload message.")
                return None

            message_type = message[4]
            if message_type != 0x04:  # Ensure it's a payload message
                print("Invalid message type in payload.")
                return None

            # Extract total segment count and current segment number
            total_segments = struct.unpack('!Q', message[5:13])[0]
            segment_number = struct.unpack('!Q', message[13:21])[0]

            # Extract the segment data (1 byte per segment as per protocol)
            segment_data = message[21:]

            return segment_number, total_segments, segment_data
        except Exception as e:
            print(f"Error parsing payload: {e}")
            return None

    def log_transfer_details(self, total_time):
        """Log transfer details after the complete file is received"""
        transfer_speed = (self.file_size * 8) / total_time  # Speed in bits per second
        print(f"UDP transfer finished, total time: {total_time:.2f} seconds, total speed: {transfer_speed:.2f} bits/second")
