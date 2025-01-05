import socket
import struct
import time
import logging

class OfferBroadcaster:
    def __init__(self, server_ip, udp_port, tcp_port):
        self.server_ip = server_ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    def start_broadcast(self):
        """Broadcast the offer message every second."""
        while True:
            offer_message = self.create_offer_message()
            self.udp_socket.sendto(offer_message, ('<broadcast>', self.udp_port))
            logging.info(f"Offer message sent to broadcast on UDP port {self.udp_port}")
            time.sleep(1)

    def create_offer_message(self):
        """Create the offer message according to the protocol."""
        message = bytearray()
        message.extend(b'\xab\xcd\xdc\xba')  # Magic cookie
        message.append(0x02)  # Offer message type
        message.extend(struct.pack('!H', self.udp_port))  # Server UDP port
        message.extend(struct.pack('!H', self.tcp_port))  # Server TCP port
        return bytes(message)
