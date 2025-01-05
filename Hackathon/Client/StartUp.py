import time

from Hackathon.Client.WaitForOffer import WaitForOffer


class StartUp:
    def __init__(self):
        self.wait_for_offer = WaitForOffer()

    def AskForDetails(self):
        try:
            user_parameters = {}
            print("Speed Test Client Setup")
            print("-----------------------")
            file_size = int(input("Enter file size in bytes: "))
            number_tcp_conn = int(input("How many TCP connections do you want to establish? "))
            number_udp_conn = int(input("How many UDP connections do you want to establish? "))

            user_parameters['file_size'] = file_size
            user_parameters['tcp'] = number_tcp_conn
            user_parameters['udp'] = number_udp_conn

            print("\nStarting client with parameters:")
            print(f"File size: {file_size} bytes")
            print(f"TCP connections: {number_tcp_conn}")
            print(f"UDP connections: {number_udp_conn}")

            self.wait_for_offer.listen(user_parameters)

            # Keep the main thread alive
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("\nShutting down client...")
                    break

        except ValueError as e:
            print(f"Invalid input: Please enter numeric values only")
        except Exception as e:
            print(f"Error during startup: {e}")