import pygame

class ExplanationWindow:
    def __init__(self, explanation, screen=None):
        # Do NOT call pygame.init() here; main.py handles it
        self.screen = screen or pygame.display.set_mode((800, 600))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.explanation = explanation
        self.font = pygame.font.SysFont("Arial", 28)
        self.running = True
        self.scroll_y = 0

        self.back_button = pygame.Rect(self.screen_width - 120, 20, 100, 40)

        # Precalculate max scroll based on text height
        self.max_scroll = 0
        self.lines = []
        self._prepare_text()

    def _prepare_text(self):
        # Wrap text and store lines so we know total height for scroll limits
        words = self.explanation.split(" ")
        max_width = self.screen_width - 100
        current_line = ""
        self.lines = []
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                self.lines.append(current_line)
                current_line = word + " "
        if current_line:
            self.lines.append(current_line)
        total_height = len(self.lines) * (self.font.get_height() + 5)
        self.max_scroll = min(0, self.screen_height - 100 - total_height)  # negative or 0

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False  # closed window

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        self.running = False
                        return True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return True
                    elif event.key == pygame.K_UP:
                        self.scroll_y = min(self.scroll_y + 20, 0)
                    elif event.key == pygame.K_DOWN:
                        self.scroll_y = max(self.scroll_y - 20, self.max_scroll)

            self.draw()
            clock.tick(60)
        return True

    def draw(self):
        self.screen.fill((245, 245, 245))

        # Draw wrapped text lines with scrolling
        y = 80 + self.scroll_y
        for line in self.lines:
            line_surf = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(line_surf, (50, y))
            y += self.font.get_height() + 5

        # Draw back button
        pygame.draw.rect(self.screen, (100, 180, 100), self.back_button)
        btn_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(btn_text, (self.back_button.x + 10, self.back_button.y + 5))

        pygame.display.flip()
