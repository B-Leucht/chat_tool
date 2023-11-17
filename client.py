import socket
import sys
import threading
from GUI import GUI  # Assuming GUI is defined in the GUI module

class ChatClient:
    def __init__(self, server_address, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, port)
        self.name = ""
        self.gui = GUI(self)

    def receive(self):
        """Handles incoming messages"""
        while True:
            data = self.s.recv(1024).decode("utf-8")
            print(data)
            if self.gui:
                self.gui.add_message(data)

    def send(self, data):
        """Ask user for their name and make sure it's not an empty string"""
        self.s.sendall(data.encode("utf-8"))

    def connect_to_server(self):
        """Connect the socket to the server and send the user's name"""
        self.name = self.gui.name
        self.s.connect(self.server_address)
        self.s.sendall(self.name.encode("utf-8")[:1024])

    def run_client(self):
        """Run the chat client"""
        self.connect_to_server()

        # Create a thread that receives incoming messages
        r_thread = threading.Thread(target=self.receive)
        r_thread.start()
        
        # Start the GUI
        self.gui.run()

if __name__ == "__main__":
    # Create a ChatClient instance and run the client
    client = ChatClient("localhost", 54321)
    client.run_client()
