import pygame

class QuestionWindow:
    def __init__(self, question, correct_answer, screen=None):
        pygame.init()
        # Use provided screen or create fullscreen
        if screen is None:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = screen

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.question = question
        self.correct_answer = correct_answer
        self.user_answer = ""
        self.font = pygame.font.SysFont("Arial", 32)
        self.running = True
        self.submitted = False
        self.correct = None  # True/False after submission

        self.input_box = pygame.Rect(self.screen_width//2 - 200, self.screen_height//2 - 20, 400, 40)
        self.submit_button = pygame.Rect(self.screen_width//2 - 60, self.screen_height//2 + 40, 120, 50)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.submitted:
                            self.running = False  # Continue to simulation
                        else:
                            self.submit_answer()
                    elif event.key == pygame.K_BACKSPACE and not self.submitted:
                        self.user_answer = self.user_answer[:-1]
                    elif not self.submitted:
                        self.user_answer += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.submit_button.collidepoint(event.pos):
                        self.submit_answer()

            self.draw()
            clock.tick(60)

        return True

    def submit_answer(self):
        if self.user_answer.strip() != "":
            try:
                user_val = float(self.user_answer)
                self.correct = abs(user_val - self.correct_answer) < 0.1
            except ValueError:
                self.correct = False
            self.submitted = True

    def draw(self):
        self.screen.fill((245, 245, 245))

        self.draw_text_wrapped(self.question, self.font, (0, 0, 0), self.screen_width//2, 150)

        pygame.draw.rect(self.screen, (220, 220, 220), self.input_box)
        answer_text = self.font.render(self.user_answer, True, (0, 0, 0))
        self.screen.blit(answer_text, (self.input_box.x + 5, self.input_box.y + 5))

        pygame.draw.rect(self.screen, (100, 180, 100), self.submit_button)
        btn_text = self.font.render("Submit", True, (255, 255, 255))
        self.screen.blit(btn_text, (self.submit_button.x + 10, self.submit_button.y + 10))

        if self.submitted:
            result = "Correct!" if self.correct else "Incorrect."
            result_text = self.font.render(result, True, (0, 0, 0))
            correct_val = self.font.render(f"Correct Answer: {self.correct_answer:.2f}", True, (0, 0, 0))
            continue_text = self.font.render("Press ENTER to continue...", True, (100, 100, 100))
            self.screen.blit(result_text, (self.screen_width//2 - 80, self.screen_height//2 + 110))
            self.screen.blit(correct_val, (self.screen_width//2 - 150, self.screen_height//2 + 150))
            self.screen.blit(continue_text, (self.screen_width//2 - 180, self.screen_height//2 + 190))

        pygame.display.flip()

    def draw_text_wrapped(self, text, font, color, x_center, y_start, max_width=None):
        if max_width is None:
            max_width = self.screen_width - 100
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
            self.screen.blit(line_surf, (x_center - line_surf.get_width()//2, y_start + i * (font.get_height() + 5)))
