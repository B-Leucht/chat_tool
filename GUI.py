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
        self.client = client
        # Pygame window properties
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255,0,0)
        self.FONT_SIZE = 20

        # Initialize Pygame window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simple Chat Tool")

        # Initialize fonts and input box properties
        self.font = pygame.font.SysFont("Courier", self.FONT_SIZE)
        self.input_box = pygame.Rect(50, self.HEIGHT - 65, self.WIDTH - 100, 32)
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.input_active = False
        self.text = [""]
        self.online_users = []
        self.current_line_idx = 0
        self.current_line = ""
        self.text_surface = self.font.render(self.text[self.current_line_idx], True, self.color)
        self.total_chat_height = 0
        self.scroll_offset = 0
        self.chat_area = pygame.Rect(50, 50, self.WIDTH - 100, self.HEIGHT - 150)
        self.chat_log = []
        self.cursor_position = 0
        # Initialize clock for controlling the frame rate
        self.clock = pygame.time.Clock()
       

    def handle_popup_events(self, popup_text, popup_active, max_width, feedback_message):
        """Handle Pygame events for the pop-up window.

        Args:
            popup_text (str): The current text entered in the pop-up window.
            popup_active (bool): Flag indicating whether the pop-up window is active.
            max_width (int): Max width of input box

        Returns:
            tuple: Updated values for popup_text and popup_active based on the events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.client:
                        response = self.client.send_name(popup_text)
                        if response == "name_taken":
                            feedback_message = "Name already taken. Please choose another name."
                        else:
                            popup_active = False
                    else:
                        popup_active = False
                elif event.key == pygame.K_BACKSPACE:
                    popup_text = popup_text[:-1]
                else:
                    if self.font.size(popup_text)[0] < max_width and event.key != pygame.K_SPACE:
                        popup_text += event.unicode
        print()
        return popup_text, popup_active, feedback_message

    def render_popup(self, popup_input_box, popup_text):
        """
        Render the pop-up window on the screen.

        Args:
            popup_input_box (pygame.Rect): The rectangle representing the pop-up window.
            popup_text (str): The text entered in the pop-up window.
        """
        self.screen.fill(self.WHITE)
        pygame.draw.rect(self.screen, self.color_active, popup_input_box, 2)

        username_text = self.font.render("Username:", True, self.BLACK)
        self.screen.blit(username_text, (popup_input_box.x + 5, popup_input_box.y - 30))

        if popup_text:
            popup_text_surface = self.font.render(popup_text, True, self.color_active)
            self.screen.blit(popup_text_surface, (popup_input_box.x + 5, popup_input_box.y + 5))

    def render_feedback_message(self, feedback_message):
        """
        Render the feedback message on the screen.

        Args:
            feedback_message (str): The feedback message to be displayed.
        """
        if feedback_message:
            feedback_message_surface = self.font.render(feedback_message, True, self.RED)
            feedback_message_rect = feedback_message_surface.get_rect()
            feedback_message_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
            self.screen.blit(feedback_message_surface, feedback_message_rect.topleft)

    def show_name_popup(self):
        """
        Display a pop-up window to get the user's name.

        Returns:
            str: The user's entered name.
        """
        popup_active = True
        popup_text = ""
        feedback_message = ""
        popup_input_box = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4, self.WIDTH // 2, 32)
        retry_count = 3  # Number of retry attempts

        while popup_active and retry_count > 0:
            popup_text, popup_active, feedback_message = self.handle_popup_events(popup_text, popup_active, popup_input_box.width - 20, feedback_message)
            self.render_popup(popup_input_box, popup_text)
            self.render_feedback_message(feedback_message)

            pygame.display.flip()
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
        wrapped_message = "\n".join(self.wrap_text([message],self.chat_area.width - 20))
        self.chat_log.append(wrapped_message)
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

    def handle_mouse_click(self, event):
        """
        Handle mouse click events.

        Parameters:
        - event (pygame.event.Event): The Pygame event object.
        """
        if self.input_box.collidepoint(event.pos):
            self.input_active = not self.input_active
        else:
            self.input_active = False
        self.color = self.color_active if self.input_active else self.color_inactive
        self.update_text_surface()

    def handle_key_press(self, event):
        """
        Handle key press events.

        Parameters:
        - event (pygame.event.Event): The Pygame event object.
        """
        if self.input_active:
            if event.key == pygame.K_RETURN:
                self.handle_return_key()
            elif event.key == pygame.K_BACKSPACE:
                self.handle_backspace_key()
            elif event.key == pygame.K_LEFT:
                self.handle_left_arrow()
            elif event.key == pygame.K_UP:
                self.line_up()
            elif event.key == pygame.K_DOWN:
                self.line_down()
            elif event.key == pygame.K_RIGHT:
                self.handle_right_arrow()
            else:
                self.handle_typing(event)
        else:
            if event.key == pygame.K_UP:
                self.scroll_up()
            elif event.key == pygame.K_DOWN:
                self.scroll_down()
                
    
    def handle_return_key(self):
        """
        Handle the Enter/Return key press event.
        """
        if self.current_line != "":
            if self.client is None:
                self.add_message(" ".join(self.text))
            else:
                self.client.send_text(" ".join(self.text))
            self.cursor_position = 0
            self.current_line_idx = 0
            self.text = [""]
            self.current_line = ""
            self.update_text_surface()

    def handle_backspace_key(self):
        """
        Handle the Backspace key press event.
        """
        if self.cursor_position:
            self.text[self.current_line_idx] = self.current_line[:self.cursor_position-1] + self.current_line[self.cursor_position:]
            # Move the cursor position to the left
            self.cursor_position -= 1
            # Update the text surface to reflect the changes
            self.handle_line_changes()
            self.update_text_surface()
        
        
    def line_up(self):

        if self.current_line_idx > 0:
            self.current_line_idx -=1
            self.current_line = self.text[self.current_line_idx]
            self.cursor_position = min(len(self.current_line), self.cursor_position)
            self.update_text_surface()

    def scroll_up(self):
        if (
                self.total_chat_height > self.chat_area.height + 5
                and self.total_chat_height - self.scroll_offset
                > self.chat_area.height
            ):
                self.scroll_offset += 20
    
    def line_down(self):
        if self.current_line_idx < len(self.text) - 1:
            self.current_line_idx += 1
            self.current_line = self.text[self.current_line_idx]
            self.cursor_position = min(len(self.current_line), self.cursor_position)
            self.update_text_surface()
            
    def scroll_down(self):
        # Scroll down if the scroll offset is greater than zero
        if self.scroll_offset > 0:
            self.scroll_offset -= 20

    def handle_left_arrow(self):
        """
        Handle the Left arrow key press event.
        """
        # Adjust the cursor position to the left
        if self.cursor_position > 0:
            self.cursor_position -= 1

        # Update the text surface to reflect the new scroll offset and cursor position
        self.handle_line_changes()
        self.update_text_surface()

    def handle_right_arrow(self):
        """
        Handle the Right arrow key press event.
        """
        # Adjust the cursor position to the right
        self.cursor_position += 1

        # Update the text surface to reflect the new scroll offset and cursor position
        self.handle_line_changes()
        self.update_text_surface()

    def handle_typing(self, event):
        """
        Handle typing events.

        Parameters:
        - event (pygame.event.Event): The Pygame event object.
        """
        if self.input_active:
            # Insert the typed character at the cursor position
            self.text[self.current_line_idx] = self.current_line[:self.cursor_position] + event.unicode + self.current_line[self.cursor_position:]
            # Move the cursor position to the right
            self.cursor_position += 1
            # Update the text surface to reflect the changes
            self.handle_line_changes()
            self.update_text_surface()

    def handle_line_changes(self):
        old_len = len(self.text)

        # Wrap the text to fit within the chat area width
        self.text = self.wrap_text(self.text, self.chat_area.width - 20)
        # Check if the cursor position is at the end of the current line
        if self.cursor_position >= len(self.current_line):
            # Move to the beginning of the next line if available
            if self.current_line_idx < len(self.text)-1:
                self.current_line_idx += 1
                self.current_line = self.text[self.current_line_idx]
                # Adjust the cursor position 
                if old_len < len(self.text):
                    self.cursor_position = len(self.current_line)
                else:
                    self.cursor_position = 0
            else:
                # Keep the cursor at the end of the current line
                self.current_line = self.text[self.current_line_idx]
                self.cursor_position = len(self.current_line)
        # Check if the cursor position is at the beginning of the text or has moved to a different line
        elif (self.cursor_position <= 0 or old_len > len(self.text)) and self.current_line_idx > 0:
            # Move to the end of the previous line if available
            self.current_line_idx -= 1
            self.current_line = self.text[self.current_line_idx]

            # Adjust the cursor position to the end of the new line
            self.cursor_position = len(self.current_line)
        # Cursor position is within the current line
        else:
            self.current_line = self.text[self.current_line_idx]

    def update_text_surface(self):
        """
        Update the text surface used for rendering the input box text.
        """

        # Render the updated line as a Pygame surface
        self.text_surface = self.font.render(self.text[self.current_line_idx], True, self.color)


    def draw_cursor_line(self):
        """
        Draw the blinking cursor line.
        """
        cursor_x = self.input_box.x + 5 + self.font.size(self.current_line[:self.cursor_position])[0]
        cursor_y = self.input_box.y + 5

        # Calculate the blinking effect using the current time
        blink_state = int(pygame.time.get_ticks() % 1000) < 500

        # Draw the cursor line if the blink state is True
        if blink_state:
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + self.FONT_SIZE),
                2,
            )
            
    def draw_ui(self):
        """
        Draw the user interface, including the chat area, input box, and cursor line.
        """
        self.screen.fill(self.WHITE)

        self.display_online_users()
        # Draw chat area and chat log
        pygame.draw.rect(self.screen, self.BLACK, self.chat_area)
        self.display_chat_log()
    
        # Draw previous line (if available)
        if self.current_line_idx > 0:
            prev_line = self.text[self.current_line_idx - 1]
            prev_line_surface = self.font.render(prev_line, True, self.color_inactive)
            self.screen.blit(
                prev_line_surface,
                (self.input_box.x + 5, self.input_box.y - self.FONT_SIZE - 5),
            )
    
        # Draw next line (if available)
        if self.current_line_idx < len(self.text) - 1:
            next_line = self.text[self.current_line_idx + 1]
            next_line_surface = self.font.render(next_line, True, self.color_inactive)
            self.screen.blit(
                next_line_surface,
                (self.input_box.x + 5, self.input_box.y + self.input_box.height + 5),
            )

        # Draw input box and input text
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        self.screen.blit(
            self.text_surface, (self.input_box.x + 5, self.input_box.y + 5)
        )

        # Draw the cursor line if the input box is active
        if self.input_active:
            self.draw_cursor_line()


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
            
    def set_online_users(self, online_users):
        self.online_users = online_users
        
    def display_online_users(self):
        """
        Display the list of online users on the screen.

        Parameters:
        - online_users (list): A list of online user names.
        """
        users = "Online Users: " + ", ".join(self.online_users)
        users = self.wrap_text([users], self.chat_area.width - 20)
        y_offset = 5
        if len(users) > 2:
            users = users[:2]
            users[1] = users[1]+"..."
        for line in users:
            user_list_surface = self.font.render(
                line, True, self.BLACK
            )
            self.screen.blit(user_list_surface, (self.input_box.x + 5, y_offset))
            y_offset += self.FONT_SIZE + 5
        
    def wrap_text(self, text, max_width):
        """wrap text into a certain max_width

        Args:
            text (list): text to be wrapped
            max_width (int): width it should be wrapped to

        Returns:
            str: wrapped text
        """
        lines = []
        words = " ".join(text).split(" ")
        current_line = ""
 
        for word in words:
            # Check if adding the current word exceeds the maximum width
            if self.font.size(current_line + " " + word)[0] <= max_width-20:
                current_line += " " + word if current_line != "" else word
            else:
                # Check if the current word itself is longer than the maximum width
                if self.font.size(word)[0] > max_width:
                    if current_line != "":
                        lines.append(current_line)
                    # Split the long word into segments that fit the maximum width
                    i=0
                    while self.font.size(word[:i])[0]<max_width:
                        i += 1
                    lines.append(word[:i])
                    current_line = ""
                else:
                    if current_line != "":
                        lines.append(current_line)
                    current_line = word

        lines.append(current_line)
        return lines

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
    gui.set_online_users(["Benny", "David"])
    gui.run()
