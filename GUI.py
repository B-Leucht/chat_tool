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
        self.total_chat_height = 0
        self.scroll_offset = 0
        self.chat_area = pygame.Rect(50, 50, self.WIDTH - 100, self.HEIGHT - 150)
        self.chat_log = []

        # Initialize clock for controlling the frame rate
        self.clock = pygame.time.Clock()
        

    def show_name_popup(self):
        """
        Display a pop-up window to get the user's name.
        """
        popup_active = True
        popup_text = ""
        popup_input_box = pygame.Rect(
            self.WIDTH // 4, self.HEIGHT // 4, self.WIDTH // 2, 32
        )
        # Continue the loop while the popup window is active
        while popup_active:
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
                        popup_active = False
                    # Check if the Backspace key is pressed
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character from the entered text
                        popup_text = popup_text[:-1]
                    else:
                        # Add the typed character to the entered text
                        if self.font.size(popup_text)[0] < popup_input_box.width-20:
                            popup_text += event.unicode
            # Fill the screen with the background color
            self.screen.fill(self.WHITE)

            # Draw the pop-up window border
            pygame.draw.rect(self.screen, self.color_active, popup_input_box, 2)

            # Render the "Username:" text on the pop-up window
            username_text = self.font.render("Username:", True, self.BLACK)
            self.screen.blit(
                username_text, (popup_input_box.x + 5, popup_input_box.y - 30)
            )

            # Render the entered text on the pop-up window
            if popup_text:
                popup_text_surface = self.font.render(popup_text, True, self.BLACK)
                self.screen.blit(
                    popup_text_surface,
                 (popup_input_box.x + 5, popup_input_box.y + 5),
                )

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            self.clock.tick(30)
        return popup_text

    def get_user_name(self):
        """
        Get the user's name using a pop-up window.

        Returns:
        - str: The user's name.
        """
        return self.show_name_popup()

    def add_message(self, message):
        """
        Add a message to the chat log.

        Parameters:
        - message (str): The message to be added.
        """
        self.chat_log.append(message)
        # Calculate the new total height of the chat log
        self.total_chat_height = int(sum(
            ((len(message.splitlines()) * (self.FONT_SIZE + 5)) + 10)
            for message in self.chat_log
        ))

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
                    # Scroll up if the total height exceeds the visible chat area
                    if (
                        self.total_chat_height > self.chat_area.height + 5
                        and self.total_chat_height - self.scroll_offset
                        > self.chat_area.height
                    ):
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
                self.add_message(self.text)
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

        # Check if there are lines in the text
        if self.text:
            self.text = self.wrap_text(self.text, self.chat_area.width - 20)
            last_line = self.text.splitlines()[-1]
            self.text_surface = self.font.render(last_line, True, self.color)
        else:
            self.text_surface = self.font.render("", True, self.color)

    def draw_ui(self):
        """
        Draw the user interface, including the chat area and input box.
        """
        self.screen.fill(self.WHITE)
        pygame.draw.rect(self.screen, self.BLACK, self.chat_area)
        self.display_chat_log()
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        self.screen.blit(
            self.text_surface, (self.input_box.x + 5, self.input_box.y + 5)
        )

    def display_chat_log(self):
        """
        Display the chat log on the screen with line breaks for long lines.
        """
        # Calculate the initial y offset for displaying chat messages
        y_offset = self.chat_area.height - 20 + self.scroll_offset

        # Iterate through each line in the reversed chat log
        for line in reversed(self.chat_log):
            lines = line.splitlines()

            # Iterate through each wrapped line in reversed order
            for line_text in reversed(lines):
                # Render the line of text as a Pygame surface
                line_surface = self.font.render(line_text, True, self.WHITE)

                # Check if the y offset is within the visible chat area
                if 0 <= y_offset <= self.chat_area.height - 20:
                    # Display the line of text on the screen at the calculated position
                    self.screen.blit(
                        line_surface,
                        (self.chat_area.x + 5, self.chat_area.y + y_offset),
                    )

                # Adjust the y offset for the next line
                y_offset -= self.FONT_SIZE + 5

            y_offset -= 10

    def wrap_text(self, text, max_width):
        """wrap text into a certain max_width

        Args:
            text (str): text to be wrapped
            max_width (int): width it should be wrapped to

        Returns:
            str: wrapped text
        """
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split(" ")
            current_line = []

            for word in words:
                # Check if adding the current word exceeds the maximum width
                if self.font.size(" ".join(current_line + [word]))[0] <= max_width:
                    current_line.append(word)
                else:
                    # Check if the current word itself is longer than the maximum width
                    if self.font.size(word)[0] > max_width:
                        # Split the long word into segments that fit the maximum width
                        i=0
                        while self.font.size(word[:i])[0]<max_width:
                            i += 1
                        lines.append(word[:i])
                        if i < len(word):
                            current_line = [word[i:]]
                        else:
                            current_line = []
                    else:
                        lines.append(" ".join(current_line))
                        current_line = [word]

            if current_line:
                lines.append(" ".join(current_line))
        return "\n".join(lines)

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
    gui.get_user_name()
    gui.run()
