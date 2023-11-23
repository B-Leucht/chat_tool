import socket
import threading
from GUI import GUI


class ChatClient:
    """
    A simple chat client that connects to a server and provides a GUI for user interaction.

    Attributes:
        s (socket.socket): The socket object for communication with the server.
        server_address (tuple): A tuple containing the server's address (host, port).
        name (str): The user's name.
        gui (GUI): An instance of the GUI class for user interface.

    Methods:
        receive(): Handles incoming messages from the server.
        send(data): Sends user input to the server.
        connect_to_server(): Connects the socket to the server and sends the user's name.
        close(): Closes the socket.
        run_client(): Runs the chat client, initializing the GUI, 
        connecting to the server, and starting a thread for receiving messages.
    """

    def __init__(self, server_address, port):
        # Initialize the chat client
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (server_address, port)
        self.name = ""
        self.gui = None

    def receive(self):
        """Handles incoming messages"""
        while True:
            try:
                # Receive incoming messages from the server
                data = self.s.recv(1024).decode("utf-8")
            except OSError:
                # Break the loop if an error occurs (e.g., socket closed)
                break
            print(data)
            if self.gui:
                # Add the received message to the GUI
                match data[0]:
                    case "t":
                        print("Hallo")
                        self.gui.add_message(data[1:])
                    case "n":
                        self.gui.set_online_users(data[1:].split(" "))

    def send_text(self, data):
        """Send user input to the server"""
        #t as firs char in string tells the server that it's a text_message
        message = "t"+data
        self.s.sendall(message.encode("utf-8"))

    def connect_to_server(self):
        """Connect the socket to the server and send the user's name"""
        # Get the user's name from the GUI
        self.name = self.gui.get_user_name()
        # Connect to the server
        self.s.connect(self.server_address)
        # Send the user's name to the server (limited to 1024 bytes)
        self.s.sendall(self.name.encode("utf-8")[:1024])

    def close(self):
        #c as first char tells the server that the client disconnected
        message = "closed" 
        self.s.sendall(message.encode("utf-8"))
        self.s.close()

    def run_client(self):
        """Run the chat client"""
        # Initialize the GUI
        self.gui = GUI(self)
        # Connect to the server
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
