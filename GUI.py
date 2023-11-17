import pygame
import sys


class GUI:
    def __init__(self, client=None):
        # Initialize Pygame
        pygame.init()
        self.client = client
        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = 20

        # Create the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simple Chat Tool")

        # Create fonts
        self.font = pygame.font.Font(None, self.FONT_SIZE)

        # Input box
        self.input_box = pygame.Rect(50, self.HEIGHT - 50, self.WIDTH - 100, 32)
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.active = False
        self.text = ""
        self.text_surface = self.font.render(self.text, True, self.color)
        self.width = max(200, self.text_surface.get_width() + 10)

        # Chat area
        self.chat_area = pygame.Rect(50, 50, self.WIDTH - 100, self.HEIGHT - 150)
        self.chat_log = []

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()
        #variables for the pop-up window
        self.popup_active = True
        self.popup_text = ""
        self.popup_input_box = pygame.Rect(self.WIDTH // 4, self.HEIGHT // 4, self.WIDTH // 2, 32)
        self.popup_color = pygame.Color("lightskyblue3")
        self.name = self.get_user_name()

    def show_name_popup(self):
        while self.popup_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.popup_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.popup_text = self.popup_text[:-1]
                    else:
                        self.popup_text += event.unicode

            self.screen.fill(self.WHITE)

            # Draw the pop-up window
            pygame.draw.rect(self.screen, self.popup_color, self.popup_input_box, 2)
            popup_text_surface = self.font.render(self.popup_text, True, self.BLACK)
            self.screen.blit(
                popup_text_surface,
                (self.popup_input_box.x + 5, self.popup_input_box.y + 5)
            )

            pygame.display.flip()
            self.clock.tick(30)

    def get_user_name(self):
        self.show_name_popup()
        return self.popup_text

    def add_message(self, message):
        self.chat_log.append(message)

    def run(self):
        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = (
                        self.color_active if self.active else self.color_inactive
                    )
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            # Process the entered text (for simplicity, just print it)
                            if self.client is None:
                                self.chat_log.append(self.text)
                            else:
                                self.client.send(self.text)
                            self.text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
                        self.width = max(200, self.font.size(self.text)[0] + 10)
                        self.text_surface = self.font.render(
                            self.text, True, self.color
                        )

            self.screen.fill(self.WHITE)

            # Draw chat area
            pygame.draw.rect(self.screen, self.BLACK, self.chat_area)

            # Display chat log
            y_offset = self.chat_area.height - 10
            for line in reversed(self.chat_log):
                line_surface = self.font.render(line, True, self.WHITE)
                self.screen.blit(
                    line_surface, (self.chat_area.x + 5, self.chat_area.y + y_offset)
                )
                y_offset -= self.FONT_SIZE + 5

            # Draw input box
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)
            self.screen.blit(
                self.text_surface, (self.input_box.x + 5, self.input_box.y + 5)
            )
            self.input_box.w = self.width

            pygame.display.flip()
            self.clock.tick(30)


# Instantiate and run the GUI
if __name__ == "__main__":
    gui = GUI()
    gui.run()
