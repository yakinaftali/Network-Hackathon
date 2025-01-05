import threading
from socket import socket

import select

from Hackathon.Client.ClientSpeedTest import ClientSpeedTest
from Hackathon.Client.OfferMessage import OfferMessage
from Hackathon.Client.RequestMessage import RequestMessage


class WaitForOffer:
    def __init__(self,user_parameters):
        # UDP socket setup for listening for server offers
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.udp_socket.bind(('', 0))
        self.speed_test = None

    def listen(self, user_parameters):
        print("Listening for server offers...")

        # Start a new thread to handle listening
        listen_thread = threading.Thread(target=self._listen_for_offers, args=(user_parameters,))
        listen_thread.daemon = True
        listen_thread.start()

    def _listen_for_offers(self, user_parameters):
        while True:
            try:
                message, address = self.udp_socket.recvfrom(1024)
                offer_mes = OfferMessage(message)

                if offer_mes:
                    print(f"Received offer from {address[0]}")

                    # Extract the server UDP and TCP ports from the offer
                    server_udp_port = offer_mes.udp_port
                    server_tcp_port = offer_mes.tcp_port

                    # Create a speed test object for this server
                    self.speed_test = ClientSpeedTest(user_parameters, offer_mes, address[0])

                    # After receiving the offer, send a request to the server
                    req_msg = RequestMessage(user_parameters['file_size'])
                    server_udp_port.sendto(bytes(req_msg), (address[0], server_udp_port))

                    # Handle the server offer (start transfer)
                    if self.speed_test:
                        self.speed_test.start()

                    break

            except Exception as e:
                print(f"Error while listening for offers: {e}")
                break

