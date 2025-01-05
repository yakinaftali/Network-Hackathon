import logging
import struct

from Hackathon.Client.Message import Message


class RequestMessage(Message):

    def __init__(self,size):
        super().__init__()
        self.sc_direction=False
        self.type_message = 0x3
        request_message = bytearray()
        request_message.extend(b'\xab\xcd\xdc\xba')
        request_message.append(self.type_message)
        request_message.extend(struct.pack('!Q', size))  # File size (8 bytes)
        self.message = request_message
