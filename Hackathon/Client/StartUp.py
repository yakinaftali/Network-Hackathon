from Hackathon.Client.WaitForOffer import WaitForOffer


class StartUp:

    def __init__(self):
        self.wait_for_offer = WaitForOffer()

    def AskForDetails(self):
        user_parameters = {}
        file_size = int(input("enter file size in bytes:"))
        number_tcp_conn = int(input("how many TCP connections do you want to establish?"))
        number_udp_conn = int(input("how many UDP connections do you want to establish?"))
        user_parameters['file_size']=file_size
        user_parameters['tcp']= number_tcp_conn
        user_parameters['udp'] = number_udp_conn
        self.wait_for_offer.listen(user_parameters)
