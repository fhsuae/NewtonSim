# explanation_window.py
import pygame

class ExplanationWindow:
    def __init__(self, explanation, screen=None):
        pygame.init()
        self.screen = screen or pygame.display.set_mode((800, 600))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.explanation = explanation
        self.font = pygame.font.SysFont("Arial", 28)
        self.running = True
        self.scroll_y = 0

        self.back_button = pygame.Rect(self.screen_width - 120, 20, 100, 40)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        self.scroll_y = min(self.scroll_y + 20, 0)
                    elif event.key == pygame.K_DOWN:
                        self.scroll_y -= 20

            self.draw()
            clock.tick(60)

    def draw(self):
        self.screen.fill((245, 245, 245))

        # Draw explanation text
        self.draw_text_wrapped(self.explanation, self.font, (0, 0, 0), 50, 80, max_width=self.screen_width - 100)

        # Draw back button
        pygame.draw.rect(self.screen, (100, 180, 100), self.back_button)
        btn_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(btn_text, (self.back_button.x + 10, self.back_button.y + 5))

        pygame.display.flip()

    def draw_text_wrapped(self, text, font, color, x_start, y_start, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines):
            line_surf = font.render(line, True, color)
            self.screen.blit(line_surf, (x_start, y_start + i * (font.get_height() + 5) + self.scroll_y))
