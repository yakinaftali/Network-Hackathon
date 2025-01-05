import logging
import struct

from Hackathon.Client.Message import Message


class RequestMessage(Message):

    def __init__(self, input_request_message: bytes):
        super().__init__()
        self.sc_direction=False
        self.type_message = 0x3


        try:
            self.cookie_Validation(input_request_message)
            logging.info("passed test of coockie validation")
            self.length_Validation(input_request_message)
            logging.info("passed test of length validation")
            self.type_Validation(input_request_message)
            logging.info("passed test of type validation")

            self.file_size = struct.unpack("!Q", input_request_message[5:13])[0]

            self.message = input_request_message
            logging.info(f"Request message successfully initialized")

        except Exception as e:
            logging.error(f"Error initializing request message: {e}")
            raise