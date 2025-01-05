import logging
from abc import ABC


class Message(ABC):

    cookie_message = bytes([0xab, 0xcd, 0xdc, 0xba])

    def __init__(self):
        self.message = None
        self.type_message = None
        self.sc_direction = None

    def cookie_Validation(self, message: bytes):
        """Validate if the message starts with the correct magic cookie."""
        if not message.startswith(self.cookie_message):
            logging.error(f"Invalid message: does not start with the required cookie {self.cookie_message.hex()}.")
            raise Exception(f"Invalid message: does not start with the required cookie {self.cookie_message.hex()}.")

    def length_Validation(self, message: bytes):
        """Validate the length of the message."""
        if self.type_message==0x2 and len(message) != 8 or self.type_message==0x3 and len(message) != 13 or self.type_message==0x4:
                logging.error(f"Invalid message: unsupported length of message {len(message)}.")
                raise Exception(f"Invalid message: unsupported length of message {len(message)}.")

    def type_Validation(self, message: bytes):
        """Validate the message type."""
        tmp_type = message[4]
        if self.type_message != tmp_type:
            logging.error(f"Invalid message type: expected 0x{self.type_message:x}, got 0x{tmp_type:x}.")
            raise Exception(f"Invalid message type: expected 0x{self.type_message:x}, got 0x{tmp_type:x}.")