import pygame

class SolutionWindow:
    def __init__(self, user_answer, correct_answer, is_correct, explanation, screen):
        self.screen = screen
        self.user_answer = user_answer
        self.correct_answer = correct_answer
        self.is_correct = is_correct
        self.explanation = explanation
        self.font = pygame.font.SysFont("Arial", 28)
        self.running = True

        self.back_button = pygame.Rect(self.screen.get_width() - 120, 20, 100, 40)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw()
            clock.tick(60)

    def draw(self):
        self.screen.fill((245, 245, 245))

        status_text = "Correct!" if self.is_correct else "Incorrect."
        status_color = (0, 150, 0) if self.is_correct else (200, 0, 0)

        self.screen.blit(self.font.render("Your Answer:", True, (0,0,0)), (50, 50))
        self.screen.blit(self.font.render(str(self.user_answer), True, (0,0,0)), (50, 90))

        self.screen.blit(self.font.render("Correct Answer:", True, (0,0,0)), (50, 150))
        self.screen.blit(self.font.render(f"{self.correct_answer:.2f}", True, (0,0,0)), (50, 190))

        self.screen.blit(self.font.render(status_text, True, status_color), (50, 250))

        self.draw_text_wrapped(self.explanation, self.font, (0, 0, 0), 50, 300, max_width=self.screen.get_width() - 100)

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
            self.screen.blit(line_surf, (x_start, y_start + i * (font.get_height() + 5)))
