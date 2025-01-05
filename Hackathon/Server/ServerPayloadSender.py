import struct
import time
import socket


class ServerPayloadSender:
    def __init__(self, file_size, udp_socket, client_address):
        self.file_size = file_size
        self.udp_socket = udp_socket
        self.client_address = client_address
        self.segment_size = 1  # 1 byte per segment as per the requirement

    def send_payload(self):
        total_segments = self.file_size // self.segment_size  # Number of segments to send
        sequence_number = 0  # Starting sequence number

        while sequence_number < total_segments:
            # Create the payload message
            payload_message = self.create_payload_message(sequence_number, total_segments)

            # Send the payload over UDP to the client
            self.udp_socket.sendto(payload_message, self.client_address)
            sequence_number += 1

            # Simulate some delay between sending segments
            time.sleep(0.1)

    def create_payload_message(self, sequence_number, total_segments):
        """Create a single payload message."""
        # Magic cookie, message type, total segments, sequence number, and payload data
        message = bytearray()
        message.extend(b'\xab\xcd\xdc\xba')  # Magic cookie
        message.append(0x04)  # Payload message type (0x04 for payload)
        message.extend(struct.pack('!Q', total_segments))  # Total segments count (8 bytes)
        message.extend(struct.pack('!Q', sequence_number))  # Current segment number (8 bytes)

        message.append(0x00)  # Placeholder for file data (1 byte)

        return bytes(message)
