import pygame
import sys

class GUI:
    """
    The GUI class represents the graphical user interface for a simple chat tool.
    """
    def __init__(self, client=None):
        """
        Initialize the GUI.

        Parameters:
        - client (object): An optional client object for handling communication.
        """
        pygame.init()

        # Pygame window properties
        self.client = client
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 20

        # Initialize Pygame window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simple Chat Tool")

        # Initialize fonts and input box properties
        self.font = pygame.font.SysFont("Courier", self.FONT_SIZE)
        self.input_box = pygame.Rect(50, self.HEIGHT - 50, self.WIDTH - 100, 32)
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.active = False
        self.text = ""
        self.text_surface = self.font.render(self.text, True, self.color)
        self.width = max(200, self.text_surface.get_width() + 10)
        self.scroll_offset = 0
        self.chat_area = pygame.Rect(50, 50, self.WIDTH - 100, self.HEIGHT - 150)
        self.chat_log = []

        # Initialize clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Name input popup properties
        self.popup_active = True
        self.popup_text = ""
        self.popup_input_box = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4, self.WIDTH // 2, 32)
        self.name = self.get_user_name()

    def show_name_popup(self):
        """
        Display a pop-up window to get the user's name.
        """
        # Continue the loop while the popup window is active
        while self.popup_active:
            # Iterate through all Pygame events
            for event in pygame.event.get():
                # Check if the event is a window close event
                if event.type == pygame.QUIT:
                    # Quit Pygame and exit the program
                    pygame.quit()
                    sys.exit()

                # Check if the event is a key down event
                if event.type == pygame.KEYDOWN:
                    # Check if the Enter/Return key is pressed
                    if event.key == pygame.K_RETURN:
                        # Disable the popup window
                        self.popup_active = False
                    # Check if the Backspace key is pressed
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character from the entered text
                        self.popup_text = self.popup_text[:-1]
                    else:
                        # Add the typed character to the entered text
                        self.popup_text += event.unicode

            # Fill the screen with the background color
            self.screen.fill(self.WHITE)

            # Draw the pop-up window border
            pygame.draw.rect(self.screen, self.color_active, self.popup_input_box, 2)

            # Render the "Username:" text on the pop-up window
            username_text = self.font.render("Username:", True, self.BLACK)
            self.screen.blit(username_text, (self.popup_input_box.x + 5, self.popup_input_box.y - 30))

            # Render the entered text on the pop-up window
            popup_text_surface = self.font.render(self.popup_text, True, self.BLACK)
            self.screen.blit(
                popup_text_surface,
                (self.popup_input_box.x + 5, self.popup_input_box.y + 5)
            )

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)


    def get_user_name(self):
        """
        Get the user's name using a pop-up window.

        Returns:
        - str: The user's name.
        """
        self.show_name_popup()
        return self.popup_text

    def add_message(self, message):
        """
        Add a message to the chat log.

        Parameters:
        - message (str): The message to be added.
        """
        self.chat_log.append(message)

    def handle_events(self):
        """
        Handle Pygame events, such as mouse clicks and key presses.
        """
        # Iterate through all Pygame events
        for event in pygame.event.get():
            # Check if the event is a window close event
            if event.type == pygame.QUIT:
                # Quit Pygame, close the client connection (if available), and exit the program
                pygame.quit()
                if self.client:
                    self.client.close()
                sys.exit()

            # Check if the event is a mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Call the method to handle mouse click events
                self.handle_mouse_click(event)

            # Check if the event is a key down event
            if event.type == pygame.KEYDOWN:
                # Call the method to handle general key press events
                self.handle_key_press(event)

                # Check if the Up arrow key is pressed
                if event.key == pygame.K_UP:
                    # Scroll up if the chat log exceeds the visible chat area
                    if len(self.chat_log) * (self.FONT_SIZE + 5) > self.chat_area.height - 20:
                        if self.scroll_offset < (len(self.chat_log) - 1) * (self.FONT_SIZE + 5):
                            self.scroll_offset += 20

                # Check if the Down arrow key is pressed
                if event.key == pygame.K_DOWN:
                    # Scroll down if the scroll offset is greater than zero
                    if self.scroll_offset > 0:
                        self.scroll_offset -= 20


    def handle_mouse_click(self, event):
        """
        Handle mouse click events.

        Parameters:
        - event (pygame.event.Event): The Pygame event object.
        """
        if self.input_box.collidepoint(event.pos):
            self.active = not self.active
        else:
            self.active = False
        self.color = self.color_active if self.active else self.color_inactive

    def handle_key_press(self, event):
        """
        Handle key press events.

        Parameters:
        - event (pygame.event.Event): The Pygame event object.
        """
        if self.active:
            if event.key == pygame.K_RETURN:
                self.handle_return_key()
            elif event.key == pygame.K_BACKSPACE:
                self.handle_backspace_key()
            else:
                self.handle_typing(event)

    def handle_return_key(self):
        """
        Handle the Enter/Return key press event.
        """
        if self.text != "":
            if self.client is None:
                self.chat_log.append(self.text)
            else:
                self.client.send_text(self.text)
            self.text = ""
            self.update_text_surface()

    def handle_backspace_key(self):
        """
        Handle the Backspace key press event.
        """
        self.text = self.text[:-1]
        self.update_text_surface()

    def handle_typing(self, event):
        """
        Handle typing events.

        Parameters:
        - event (pygame.event.Event): The Pygame event object.
        """
        self.text += event.unicode
        self.update_text_surface()

    def update_text_surface(self):
        """
        Update the text surface used for rendering the input box text.
        """
        lines = self.wrap_text(self.text, self.chat_area.width - 10)
        last_line = lines[-1]
        self.width = max(200, self.font.size(last_line)[0] + 10)
        self.text_surface = self.font.render(last_line, True, self.color)

    def draw_ui(self):
        """
        Draw the user interface, including the chat area and input box.
        """
        self.screen.fill(self.WHITE)
        pygame.draw.rect(self.screen, self.BLACK, self.chat_area)
        self.display_chat_log()
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        self.screen.blit(self.text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.input_box.w = self.width

    def display_chat_log(self):
        """
        Display the chat log on the screen with line breaks for long lines.
        """
        # Calculate the initial y offset for displaying chat messages
        y_offset = self.chat_area.height - 20 + self.scroll_offset

        # Iterate through each line in the reversed chat log
        for line in reversed(self.chat_log):
        # Wrap the text to fit within the specified width
            lines = self.wrap_text(line, self.chat_area.width - 10)

            # Iterate through each wrapped line in reversed order
            for line_text in reversed(lines):
                # Render the line of text as a Pygame surface
                line_surface = self.font.render(line_text, True, self.WHITE)

                # Check if the y offset is within the visible chat area
                if 0 <= y_offset <= self.chat_area.height - 20:
                    # Display the line of text on the screen at the calculated position
                    self.screen.blit(
                        line_surface, (self.chat_area.x + 5, self.chat_area.y + y_offset)
                    )

                # Adjust the y offset for the next line
                y_offset -= self.FONT_SIZE + 5
            
    def wrap_text(self, text, max_width):
        """
        Wrap the text to fit within the specified width.

        Parameters:
        - text (str): The text to wrap.
        - max_width (int): The maximum width for the wrapped text.

        Returns:
        - list: A list of wrapped lines.
        """
        # Split the input text into a list of words
        words = text.split(' ')

        # Initialize variables for wrapped lines and the current line
        wrapped_lines = []
        current_line = words[0]

        # Iterate through each word in the text
        for word in words[1:]:
            # Concatenate the current line with the next word
            test_line = current_line + ' ' + word

            # Get the width and height of the test line using the Pygame font
            width, _ = self.font.size(test_line)
            # If the current line itself exceeds the max_width, add it to wrapped_lines
            # Check if the test line fits within the specified width
            if width <= max_width:
                # Update the current line with the test line if it fits
                    current_line = test_line
            else:
                # Add the current line to the list of wrapped lines
                wrapped_lines.append(current_line)

                # Reset the current line to the current word
                current_line = word

        # Add the last remaining line to the list of wrapped lines
        wrapped_lines.append(current_line)

        # Return the list of wrapped lines
        return wrapped_lines



    def run(self):
        """
        Run the main loop for the GUI.
        """
        while True:
            self.handle_events()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    gui = GUI()
    gui.run()
