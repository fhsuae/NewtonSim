import pygame

class QuestionWindow:
    def __init__(self, screen, question, correct_answer):
        self.screen = screen
        self.question = question
        self.correct_answer = correct_answer
        self.user_answer = ""
        self.font = pygame.font.SysFont("Arial", 28)
        self.running = True
        self.submitted = False
        self.correct = None  # True/False after submission

    def run(self):
        clock = pygame.time.Clock()
        input_box = pygame.Rect(200, 300, 400, 40)
        submit_button = pygame.Rect(350, 370, 100, 40)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False  # Quit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.submit_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_answer = self.user_answer[:-1]
                    elif not self.submitted:
                        self.user_answer += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_button.collidepoint(event.pos):
                        self.submit_answer()

            self.draw(input_box, submit_button)
            clock.tick(60)

        return True  # Continue to simulation

    def submit_answer(self):
        if self.user_answer.strip() != "":
            try:
                user_val = float(self.user_answer)
                self.correct = abs(user_val - self.correct_answer) < 0.1
            except ValueError:
                self.correct = False
            self.submitted = True

    def draw(self, input_box, submit_button):
        self.screen.fill((245, 245, 245))
        question_text = self.font.render(self.question, True, (0, 0, 0))
        self.screen.blit(question_text, (100, 200))

        # Input box
        pygame.draw.rect(self.screen, (220, 220, 220), input_box)
        answer_text = self.font.render(self.user_answer, True, (0, 0, 0))
        self.screen.blit(answer_text, (input_box.x + 5, input_box.y + 5))

        # Submit button
        pygame.draw.rect(self.screen, (100, 180, 100), submit_button)
        btn_text = self.font.render("Submit", True, (255, 255, 255))
        self.screen.blit(btn_text, (submit_button.x + 10, submit_button.y + 5))

        if self.submitted:
            result = "Correct!" if self.correct else "Incorrect."
            result_text = self.font.render(result, True, (0, 0, 0))
            correct_val = self.font.render(f"Correct Answer: {self.correct_answer:.2f}", True, (0, 0, 0))
            continue_text = self.font.render("Press ENTER to continue...", True, (100, 100, 100))
            self.screen.blit(result_text, (300, 430))
            self.screen.blit(correct_val, (250, 470))
            self.screen.blit(continue_text, (230, 510))

        pygame.display.flip()
