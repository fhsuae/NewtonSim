import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)

    def run(self):
        while True:
            self.screen.fill((200, 200, 200))
            title = self.font.render("Physics Simulator", True, (0, 0, 0))
            pendulum_text = self.font.render("1. Pendulum", True, (0, 0, 0))
            quit_text = self.font.render("2. Quit", True, (0, 0, 0))

            self.screen.blit(title, (250, 100))
            self.screen.blit(pendulum_text, (300, 250))
            self.screen.blit(quit_text, (300, 320))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "pendulum"
                    elif event.key == pygame.K_2:
                        return "quit"
