import pygame
import sys

class GUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

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
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.text_surface = self.font.render(self.text, True, self.color)
        self.width = max(200, self.text_surface.get_width() + 10)

        # Chat area
        self.chat_area = pygame.Rect(50, 50, self.WIDTH - 100, self.HEIGHT - 150)
        self.chat_log = []

        # Clock to control the frame rate
        self.clock = pygame.time.Clock()

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
                    self.color = self.color_active if self.active else self.color_inactive
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            # Process the entered text (for simplicity, just print it)
                            print(self.text)
                            self.chat_log.append(self.text)
                            self.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
                        self.width = max(200, self.font.size(self.text)[0] + 10)
                        self.text_surface = self.font.render(self.text, True, self.color)

            self.screen.fill(self.WHITE)

            # Draw chat area
            pygame.draw.rect(self.screen, self.BLACK, self.chat_area)

            # Display chat log
            y_offset = self.chat_area.height - 10
            for line in reversed(self.chat_log):
                line_surface = self.font.render(line, True, self.WHITE)
                self.screen.blit(line_surface, (self.chat_area.x + 5, self.chat_area.y + y_offset))
                y_offset -= self.FONT_SIZE + 5

            # Draw input box
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)
            self.screen.blit(self.text_surface, (self.input_box.x + 5, self.input_box.y + 5))
            self.input_box.w = self.width

            pygame.display.flip()
            self.clock.tick(30)

# Instantiate and run the GUI
if __name__ == "__main__":
    gui = GUI()
    gui.run()
