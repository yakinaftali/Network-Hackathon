import struct
import time
import socket


class ClientPayloadReceiver:
    def __init__(self, udp_socket, expected_file_size):
        self.udp_socket = udp_socket
        self.expected_file_size = expected_file_size
        self.received_data = 0
        self.expected_segments = self.expected_file_size // 1  # 1 byte per segment

    def receive_payload(self):
        last_time_received = time.time()
        received_segments = set()

        while True:
            try:
                # Receive UDP packet
                message, address = self.udp_socket.recvfrom(1024)

                # Extract the payload message
                payload = self.parse_payload(message)

                if payload:
                    segment_number, total_segments, data = payload
                    received_segments.add(segment_number)
                    self.received_data += len(data)

                    # Print the progress
                    print(f"Received segment {segment_number}/{total_segments}")

                    # Check if all segments are received
                    if len(received_segments) == total_segments:
                        print("All segments received, transfer complete.")
                        break

                    # If no data is received for 1 second, end the UDP transfer (Timeout)
                    last_time_received = time.time()

                if time.time() - last_time_received > 1:
                    print("No data received for 1 second, ending transfer.")
                    break

            except Exception as e:
                print(f"Error while receiving payload: {e}")
                break

        # Log the transfer stats (Time and Speed)
        self.log_transfer_stats()

    def parse_payload(self, message):
        """Parse the incoming payload message."""
        try:
            # Extract and validate magic cookie and message type
            magic_cookie = message[:4]
            if magic_cookie != b'\xab\xcd\xdc\xba':
                print("Invalid magic cookie in payload message.")
                return None

            message_type = message[4]
            if message_type != 0x04:  # 0x04 means Payload message type
                print("Invalid message type in payload.")
                return None

            # Extract total segment count and segment number
            total_segments = struct.unpack('!Q', message[5:13])[0]
            segment_number = struct.unpack('!Q', message[13:21])[0]

            # Extract payload data (1 byte as specified)
            data = message[21:]

            return segment_number, total_segments, data
        except Exception as e:
            print(f"Error parsing payload: {e}")
            return None

    def log_transfer_stats(self):
        """Log the transfer stats after receiving all segments."""
        total_time = time.time() - self.start_time
        speed = (self.received_data * 8) / total_time  # Calculate speed in bits per second
        print(f"UDP transfer finished, total time: {total_time:.2f} seconds, total speed: {speed:.2f} bits/second")
