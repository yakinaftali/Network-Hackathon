from Hackathon.Client.TCPTrans import TCPTrans
from Hackathon.Client.UDPTrans import UDPTrans


class ClientSpeedTest:
    """
     This class is responsible for starting the speed test by managing both TCP and UDP file transfers.
    """
    def __init__(self, user_parameters,offer_msg,server_ip):
        """
        Initialize with user parameters (such as the file size and number of connections)
        and server details (UDP and TCP ports obtained from the OfferMessage
        :param user_parameters:
        :param offer_msg:
        """
        self.user_parameters = user_parameters
        self.server_ip = server_ip
        self.server_udp_port = offer_msg.udp_port
        self.server_tcp_port = offer_msg.tcp_port

    def start_speed_test(self):
        """
        tarts the speed test by creating multiple
        TCPTrans and UDPTrans objects based on the number of TCP and UDP connections the user wants
        :return:
        """
        tcp_connections = self.user_parameters['tcp']
        udp_connections = self.user_parameters['udp']

        # Create TCP transfers
        for _ in range(tcp_connections):
            tcp_transfer = TCPTrans(self.server_ip, self.server_tcp_port, self.user_parameters['file_size'])
            tcp_transfer.start()

        # Create UDP transfers
        for _ in range(udp_connections):
            udp_transfer = UDPTrans(self.server_ip, self.server_udp_port, self.user_parameters['file_size'])
            udp_transfer.start()
