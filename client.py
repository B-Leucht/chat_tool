import socket
import sys
import threading
from GUI import GUI  # Assuming GUI is defined in the GUI module

class ChatClient:
    def __init__(self, server_address, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, port)
        self.name = ""
        self.gui = None

    def receive(self):
        """Handles incoming messages"""
        while True:
            data = self.s.recv(1024).decode("utf-8")
            print(data)
            if self.gui:
                self.gui.add_message(data)

    def get_user_name(self):
        """Ask user for their name and make sure it's not an empty string"""
        while self.name == "":
            self.name = input("Name: ")

    def connect_to_server(self):
        """Connect the socket to the server and send the user's name"""
        self.s.connect(self.server_address)
        self.s.sendall(self.name.encode("utf-8")[:1024])

    def start_gui(self):
        """Start the GUI"""
        self.gui = GUI(self.s)
        self.gui.run()

    def run_client(self):
        """Run the chat client"""
        self.get_user_name()
        self.connect_to_server()

        # Create a thread that receives incoming messages
        r_thread = threading.Thread(target=self.receive)
        r_thread.start()

        # Start the GUI
        self.start_gui()

        # Get user input and send it to the server
        while True:
            line = input()
            if line != "":
                self.s.sendall(line.encode("utf-8"))

if __name__ == "__main__":
    # Create a ChatClient instance and run the client
    client = ChatClient("localhost", 54321)
    client.run_client()
