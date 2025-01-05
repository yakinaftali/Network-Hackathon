from abc import ABC, abstractmethod
from datetime import time


class Transfer(ABC):

    def __init__(self, ip, port, size):
        self.server_ip = ip
        self.server_port = port
        self.file_size = size
        self.start_time = None

    @abstractmethod
    def start(self):
        """Start the transfer"""
        pass

    @abstractmethod
    def calculate_transfer_speed(self):
        """Calculate the transfer speed in bits per second"""
        if self.start_time is None:
            return 0
        transfer_speed = (self.file_size * 8) / (time.time() - self.start_time)
        return transfer_speed

    def log_transfer_details(self, total_time):
        """Log common transfer details (e.g., time, speed, and success rate)"""
        speed = self.calculate_transfer_speed()
        print(f"{self.__class__.__name__} transfer finished, total time: {total_time:.2f} seconds, total speed: {speed:.2f} bits/second")
