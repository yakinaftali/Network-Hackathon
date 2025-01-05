import socket
import threading

import select

from Hackathon.Client.ClientSpeedTest import ClientSpeedTest
from Hackathon.Client.OfferMessage import OfferMessage
from Hackathon.Client.RequestMessage import RequestMessage


class WaitForOffer:
    def __init__(self):  # Remove user_parameters parameter
        # UDP socket setup for listening for server offers
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.udp_socket.bind(('', 0))  # Bind to any available port
        self.speed_test = None

    def listen(self, user_parameters):
        print("Listening for server offers...")
        print(f"Listening on port {self.udp_socket.getsockname()[1]}")

        # Start a new thread to handle listening
        listen_thread = threading.Thread(target=self._listen_for_offers, args=(user_parameters,))
        listen_thread.daemon = True
        listen_thread.start()

    def _listen_for_offers(self, user_parameters):
        while True:
            try:
                # Use select with timeout to avoid blocking indefinitely
                ready = select.select([self.udp_socket], [], [], 1.0)
                if ready[0]:
                    message, address = self.udp_socket.recvfrom(1024)
                    print(f"Received message from {address}")

                    try:
                        offer_mes = OfferMessage(message)
                        print(f"Received valid offer from {address[0]}")
                        print(f"Server UDP Port: {offer_mes.udp_port}")
                        print(f"Server TCP Port: {offer_mes.tcp_port}")

                        # Create a speed test object for this server
                        self.speed_test = ClientSpeedTest(user_parameters, offer_mes, address[0])

                        # Send request using the UDP socket we already have
                        req_msg = RequestMessage(user_parameters['file_size'])
                        self.udp_socket.sendto(bytes(req_msg), (address[0], offer_mes.udp_port))
                        print(f"Sent request message to server at {address[0]}:{offer_mes.udp_port}")

                        # Start the speed test
                        if self.speed_test:
                            print("Starting speed test...")
                            self.speed_test.start()
                            break
                    except Exception as e:
                        print(f"Error processing offer message: {e}")
                        continue

            except Exception as e:
                print(f"Error while listening for offers: {e}")
                break