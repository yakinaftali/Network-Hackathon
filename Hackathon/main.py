import threading
import time
from Hackathon.Server.Server import Server
from Hackathon.Server.OfferBroadcaster import OfferBroadcaster
from Hackathon.Server.TCPHandler import TCPHandler
from Hackathon.Server.UDPHandler import UDPHandler

def main():
    # Server parameters
    server_ip = '0.0.0.0'  # Can use 'localhost' or a specific IP address
    tcp_port = 12345        # Example TCP port for file transfer
    udp_port = 12346        # Example UDP port for broadcasting offers
    file_size = 10485760    # File size in bytes (e.g., 10 MB)

    # Create the server instance
    server = Server(server_ip, tcp_port, udp_port, file_size)

    # Create and start the OfferBroadcaster to send offer messages over UDP
    offer_broadcaster = OfferBroadcaster(server_ip, udp_port, tcp_port)
    offer_broadcaster_thread = threading.Thread(target=offer_broadcaster.start_broadcast)
    offer_broadcaster_thread.daemon = True
    offer_broadcaster_thread.start()

    # Start the server to listen for incoming TCP/UDP connections
    server.start()

if __name__ == "__main__":
    main()
