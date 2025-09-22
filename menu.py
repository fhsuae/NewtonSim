import pygame

class Button:
    def __init__(self, rect, text, font, bg_color=(180, 180, 180), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # border
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)

        # Defines the buttons
        self.pendulum_button = Button((300, 220, 200, 60), "Pendulum", self.font)
        self.spring_button   = Button((300, 300, 200, 60), "Spring",   self.font)
        self.quit_button     = Button((300, 380, 200, 60), "Quit",     self.font)

    def run(self):
        while True:
            self.screen.fill((200, 200, 200))
            title = self.font.render("Physics Simulator", True, (0, 0, 0))
            self.screen.blit(title, (250, 100))

            # draws the buttons
            self.pendulum_button.draw(self.screen)
            self.spring_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if self.pendulum_button.is_clicked(event):
                    return "pendulum"
                if self.spring_button.is_clicked(event):
                    return "spring"
                if self.quit_button.is_clicked(event):
                    return "quit"
