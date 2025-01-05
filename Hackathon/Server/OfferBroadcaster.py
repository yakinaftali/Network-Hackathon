import socket
import platform
import struct
import time


class OfferBroadcaster:
    """
    Responsible for broadcasting an "offer" message to any clients on the network using UDP.
    """

    def __init__(self, server_ip, udp_port, tcp_port):
        self.server_ip = server_ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start_broadcast(self):
        """Broadcast the offer message every second."""
        while True:
            offer_message = self.create_offer_message()
            self.udp_socket.sendto(offer_message, ('<broadcast>', self.udp_port))
            print(f"Offer message sent to broadcast on UDP port {self.udp_port}")
            time.sleep(1)

    def create_offer_message(self):
        """Create the offer message according to the protocol."""
        message = bytearray()
        message.extend(b'\xab\xcd\xdc\xba')  # Magic cookie
        message.append(0x02)  # Message type for offer
        message.extend(struct.pack('!H', self.udp_port))  # UDP port
        message.extend(struct.pack('!H', self.tcp_port))  # TCP port
        return bytes(message)
