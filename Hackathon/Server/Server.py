import threading
import socket
import select

from Hackathon.Server.OfferBroadcaster import OfferBroadcaster
from Hackathon.Server.TCPHandler import TCPHandler
from Hackathon.Server.UDPHandler import UDPHandler


class Server:
    """
    Core class that handles both TCP and UDP connections from clients.
    """
    def __init__(self, ip, tcp_port, udp_port, file_size):
        self.ip = ip
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.file_size = file_size
        self.udp_socket = None
        self.tcp_socket = None

    def start(self):
        # Start UDP offer broadcaster (as shown before)
        offer_broadcaster = OfferBroadcaster(self.ip, self.udp_port, self.tcp_port)
        threading.Thread(target=offer_broadcaster.start_broadcast, daemon=True).start()  # Start offer broadcast in a separate thread

        # Start listening for connections and handle them
        self.listen_for_connections()

    def listen_for_connections(self):
        """Listen for both TCP and UDP connections."""
        # Handling TCP
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((self.ip, self.tcp_port))
        self.tcp_socket.listen(5)
        print(f"Server started, listening on IP address {self.ip}:{self.tcp_port}")

        # Handling UDP
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.ip, self.udp_port))
        print(f"Server started, listening on UDP port {self.udp_port}")

        while True:
            # Using select to avoid blocking indefinitely
            readable, _, _ = select.select([self.tcp_socket, self.udp_socket], [], [], 1)  # Timeout of 1 second

            # Handle TCP connections if ready
            if self.tcp_socket in readable:
                tcp_conn, tcp_addr = self.tcp_socket.accept()
                print(f"Received TCP connection from {tcp_addr}")
                tcp_handler = TCPHandler(tcp_conn, self.file_size)
                threading.Thread(target=tcp_handler.start).start()

            # Handle UDP requests if ready
            if self.udp_socket in readable:
                rlist, _, _ = select.select([self.udp_socket], [], [], 1)  # Timeout of 1 second
                if rlist:
                    data, udp_addr = self.udp_socket.recvfrom(1024)
                    print(f"Received UDP request from {udp_addr}")
                    udp_handler = UDPHandler(data, udp_addr, self.file_size, self.udp_socket)
                    threading.Thread(target=udp_handler.start).start()
