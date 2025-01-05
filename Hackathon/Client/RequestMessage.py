import logging
import struct

from Hackathon.Client.Message import Message


class RequestMessage(Message):

    def __init__(self,size):
        super().__init__()
        #8 bytes
        if size < 0 or size > (2 ** 64 - 1):
            raise
        self.sc_direction=False
        self.type_message = 0x3
        request_message = bytearray()
        request_message.extend(b'\xab\xcd\xdc\xba')
        request_message.append(self.type_message)
        request_message.extend(struct.pack('!Q', size))
        self.message = request_message
