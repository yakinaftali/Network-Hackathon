from Hackathon.Server.ServerPayloadSender import ServerPayloadSender


class UDPHandler:
    def __init__(self, data, udp_addr, file_size, udp_socket):
        self.data = data
        self.udp_addr = udp_addr
        self.file_size = file_size
        self.udp_socket = udp_socket

    def start(self):
        # Create ServerPayloadSender instance to send the file over UDP
        payload_sender = ServerPayloadSender(self.file_size, self.udp_socket, self.udp_addr)
        payload_sender.send_payload()
