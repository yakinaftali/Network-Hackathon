class StartUp:

    def __init__(self,data):
        self.data=data
        self.wait_for_offer =  WaitForOffer()

    def AskForDetails():
        user_parameters={}
        self.wait_for_offer.listen(user_parameters)
