import pygame

class Button:
    def __init__(self, rect, text, font, bg_color=(180, 180, 180), hover_color=(220, 220, 220), text_color=(0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = bg_color
        self.hovered = False

    def draw(self, screen):
        #  color transtion
        target_color = self.hover_color if self.hovered else self.bg_color
        self.current_color = tuple(
            int(self.current_color[i] + (target_color[i] - self.current_color[i]) * 0.2)
            for i in range(3)
        )

        #  Size increase when hovered
        scale = 1.1 if self.hovered else 1.0
        scaled_rect = self.rect.copy()
        scaled_rect.width = int(self.rect.width * scale)
        scaled_rect.height = int(self.rect.height * scale)
        scaled_rect.center = self.rect.center

        pygame.draw.rect(screen, self.current_color, scaled_rect)
        pygame.draw.rect(screen, (0, 0, 0), scaled_rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

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

        self.pendulum_button = Button((300, 220, 200, 60), "Pendulum", self.font)
        self.spring_button   = Button((300, 300, 200, 60), "Spring",   self.font)
        self.quit_button     = Button((300, 380, 200, 60), "Quit",     self.font)

    def run(self):
        while True:
            self.screen.fill((200, 200, 200))
            title = self.font.render("Physics Simulator", True, (0, 0, 0))
            self.screen.blit(title, (250, 100))

            mouse_pos = pygame.mouse.get_pos()
            self.pendulum_button.update_hover(mouse_pos)
            self.spring_button.update_hover(mouse_pos)
            self.quit_button.update_hover(mouse_pos)

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
