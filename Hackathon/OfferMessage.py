import logging
class OfferMessage(Message):


    def __init__(self, input_offer_message: bytes):
        super().__init__()
        self.sc_direction=True
        self.type_message = 0x2

        try:
            self.cookie_Validation(input_offer_message)
            logging.info("passed test of coockie validation")
            self.length_Validation(input_offer_message)
            logging.info("passed test of length validation")
            self.type_Validation(input_offer_message)
            logging.info("passed test of type validation")

            self.udp_port = struct.unpack("!H", input_offer_message[5:7])[0]
            logging.info("udp port succesffuly extractef")
            self.tcp_port = struct.unpack("!H", input_offer_message[7:9])[0]
            logging.info("tcp port succesffuly extractef")

            self.message = input_offer_message
            logging.info(f"Offer message successfully initialized")

        except Exception as e:
            logging.error(f"Error initializing offer message: {e}")
            raise
