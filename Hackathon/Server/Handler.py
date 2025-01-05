from abc import ABC, abstractmethod
import time

class Handler(ABC):
    def __init__(self, file_size, start_time=None):
        self.file_size = file_size
        self.start_time = start_time or time.time()

    @abstractmethod
    def start(self):
        """Start the transfer process. To be implemented by subclass."""
        pass

    def calculate_speed(self, total_time):
        """Calculate the transfer speed in bits/second."""
        return (self.file_size * 8) / total_time

    def log_transfer_info(self, transfer_type, total_time):
        """Log common transfer information like time and speed."""
        print(f"{transfer_type} transfer finished, total time: {total_time:.2f} seconds, "
              f"total speed: {self.calculate_speed(total_time):.2f} bits/second")
