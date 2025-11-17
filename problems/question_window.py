import pygame


class QuestionWindow:
    def __init__(self, question, correct_answer, screen=None, hints=None):
        self.screen = screen or pygame.display.set_mode((800, 600))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.question = question
        self.correct_answer = correct_answer
        self.user_answer = ""
        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.running = True
        self.submitted = False
        self.correct = None
        self.hints = hints or []
        self.hint_index = 0
        self.showing_hint = False

        self.attempts = 0
        self.max_attempts = 5
        self.attempts_exceeded = False

        # UI elements
        self.input_box = pygame.Rect(self.screen_width // 2 - 200, self.screen_height // 2 - 20, 400, 40)
        self.submit_button = pygame.Rect(self.screen_width // 2 - 60, self.screen_height // 2 + 40, 120, 50)
        self.hint_button = pygame.Rect(self.screen_width // 2 + 150, self.screen_height // 2 + 40, 120, 50)

        # Cursor
        self.cursor_visible = True
        self.cursor_timer = 0.0

    def run(self):
        clock = pygame.time.Clock()
        result = {
            "continue_to_sim": False,
            "correct": False,
            "user_answer": None,
            "closed": False,
            "attempts_exceeded": False
        }

        while self.running:
            dt = clock.tick(60) / 1000.0
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result["closed"] = True
                    self.running = False
                    break

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        result["closed"] = True
                        self.running = False
                        break

                    if not self.submitted:
                        if event.key == pygame.K_RETURN:
                            self._submit_answer()
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_answer = self.user_answer[:-1]
                        else:
                            if event.unicode and len(event.unicode) == 1 and (event.unicode.isdigit() or event.unicode in ['.', '-', '+', 'e']):
                                self.user_answer += event.unicode

                    else:
                        if self.correct and event.key == pygame.K_RETURN:
                            result["continue_to_sim"] = True
                            result["correct"] = True
                            result["user_answer"] = self._parse_answer_for_result()
                            self.running = False
                            break

                        if not self.correct and event.key == pygame.K_RETURN:
                            # After incorrect submission, allow retry by resetting submitted
                            self.submitted = False
                            self.showing_hint = False
                            self.user_answer = ""

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.submitted:
                        if self.submit_button.collidepoint(event.pos):
                            self._submit_answer()
                        elif self.hint_button.collidepoint(event.pos):
                            self._show_next_hint()
                    else:
                        if self.correct:
                            # If correct: pressing anywhere goes to simulation for simplicity
                            result["continue_to_sim"] = True
                            result["correct"] = True
                            result["user_answer"] = self._parse_answer_for_result()
                            self.running = False
                            break
                        else:
                            # Incorrect but submitted: clicking submit again resets for retry
                            self.submitted = False
                            self.showing_hint = False
                            self.user_answer = ""

            # If attempts exceeded, auto-move on to explanation
            if self.attempts_exceeded:
                result["attempts_exceeded"] = True
                self.running = False
                break

            self.draw()

        if not result["closed"]:
            result["correct"] = bool(self.correct)
            result["user_answer"] = self._parse_answer_for_result()

        return result

    def _submit_answer(self):
        if self.user_answer.strip() == "":
            return
        self.attempts += 1
        if self.attempts > self.max_attempts:
            self.attempts_exceeded = True
            return
        try:
            user_val = float(self.user_answer)
            self.correct = abs(user_val - self.correct_answer) < 0.1
        except ValueError:
            self.correct = False

        self.submitted = True
        self.showing_hint = False

    def _show_next_hint(self):
        if self.hints and self.hint_index < len(self.hints):
            self.hint_index += 1
            self.showing_hint = True

    def _parse_answer_for_result(self):
        try:
            return float(self.user_answer)
        except Exception:
            return self.user_answer

    def draw(self):
        self.screen.fill((245, 245, 245))

        # Draw question text
        self.draw_text_wrapped(self.question, self.font, (0, 0, 0), self.screen_width // 2, 80,
                               max_width=self.screen_width - 120)

        # Input box
        pygame.draw.rect(self.screen, (220, 220, 220), self.input_box)
        answer_text = self.font.render(self.user_answer, True, (0, 0, 0))
        self.screen.blit(answer_text, (self.input_box.x + 8, self.input_box.y + 6))

        # Cursor
        if not self.submitted and self.cursor_visible:
            cursor_x = self.input_box.x + 8 + answer_text.get_width() + 2
            cursor_y = self.input_box.y + 8
            pygame.draw.rect(self.screen, (0, 0, 0), (cursor_x, cursor_y, 2, self.font.get_height() - 4))

        # Submit Button
        pygame.draw.rect(self.screen, (100, 180, 100), self.submit_button)
        btn_text = self.small_font.render("Submit", True, (255, 255, 255))
        self.screen.blit(btn_text, (self.submit_button.x + 20, self.submit_button.y + 12))

        # Hint Button
        pygame.draw.rect(self.screen, (100, 100, 220), self.hint_button)
        hint_text = self.small_font.render("Hint", True, (255, 255, 255))
        self.screen.blit(hint_text, (self.hint_button.x + 35, self.hint_button.y + 12))

        # Status messages
        if self.submitted:
            if self.correct:
                msg = "Correct! Press ENTER to continue."
                color = (0, 150, 0)
            else:
                if self.attempts >= self.max_attempts:
                    msg = f"Max attempts reached ({self.max_attempts}). Moving on..."
                else:
                    msg = "Incorrect. Try again or ask for a hint."
                color = (200, 0, 0)

            status_text = self.font.render(msg, True, color)
            self.screen.blit(status_text, (self.screen_width // 2 - status_text.get_width() // 2, self.screen_height // 2 + 80))

        # Show hints if requested
        if self.showing_hint and self.hint_index > 0:
            hint_text_lines = "\n".join(self.hints[:self.hint_index])
            self.draw_text_wrapped(f"Hints:\n{hint_text_lines}", self.small_font, (0, 0, 180), self.screen_width // 2,
                                   self.screen_height // 2 + 140, max_width=self.screen_width - 120)

        # Instructions
        inst = self.small_font.render("Type numeric answer, Submit or ENTER to submit. ESC to cancel.", True, (80, 80, 80))
        self.screen.blit(inst, (20, self.screen_height - 40))

        pygame.display.flip()

    def draw_text_wrapped(self, text, font, color, x_center, y_start, max_width=None):
        if max_width is None:
            max_width = self.screen_width - 100
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (word + " ")
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines):
            line_surf = font.render(line.strip(), True, color)
            self.screen.blit(line_surf, (x_center - line_surf.get_width() // 2, y_start + i * (font.get_height() + 6)))
