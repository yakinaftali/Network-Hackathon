class PayloadMessage(Message):

    def __init__(self, input_payload_message: bytes):
        super().__init__()
        self.type_message = 0x4
        self.sc_direction=True


        try:
            self.cookie_Validation(input_offer_message)
            logging.info("passed test of coockie validation")
            self.length_Validation(input_offer_message)
            logging.info("passed test of length validation")
            self.type_Validation(input_offer_message)
            logging.info("passed test of type validation")

            self.total_segments = struct.unpack("!Q", input_payload_message[5:13])[0]
            logging.info(f"total segment number extracted succesfully")

            self.current_segment = struct.unpack("!Q", input_payload_message[13:21])[0]
            logging.info(f"current segment number extracted succesfully")
            self.payload_data = input_payload_message[21:]
            logging.info(f"payload data extracted succesfully")
            self.message = input_payload_message
            logging.info(f"Payload message successfully initialized")

        except Exception as e:
            logging.error(f"Error initializing payload message: {e}")
            raise