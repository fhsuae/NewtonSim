import pygame

class Slider:
    def __init__(self, x, y, width, min_val=0.0, max_val=2.0, initial=0.1, label=""):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.handle_pos = x + (initial - min_val) / (max_val - min_val) * width
        self.dragging = False
        self.label = label
        self.font = pygame.font.SysFont("Arial", 18)

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        pygame.draw.circle(screen, (50, 50, 200), (int(self.handle_pos), self.rect.centery), 10)
        text = self.font.render(f"{self.label}: {self.value:.2f}", True, (0, 0, 0))
        screen.blit(text, (self.rect.x, self.rect.y - 25))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.handle_pos - 10, self.rect.centery - 10, 20, 20).collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_pos = max(self.rect.left, min(self.rect.right, event.pos[0]))
            t = (self.handle_pos - self.rect.left) / self.rect.width
            self.value = self.min_val + t * (self.max_val - self.min_val)


class SpringSim:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.anchor = (200, 300)
        self.rest_length = 150
        self.mass_radius = 20
        self.font = pygame.font.SysFont("Arial", 18)

        self.speed_slider = Slider(50, 550, 200, 0.1, 2.0, 1.0, label="Speed")
        self.resistance_slider = Slider(300, 550, 200, 0.0, 2.0, 0.1, label="Resistance")

        self.reset()

    def reset(self):
        self.pos = 100.0
        self.v = 0.0
        self.k = 20.0
        self.m = 1.0
        self.dragging = False

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mass_x = int(self.anchor[0] + self.rest_length + self.pos)
        mass_y = self.anchor[1]
        reset_rect = pygame.Rect(700, 10, 80, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if abs(mouse_x - mass_x) < self.mass_radius and abs(mouse_y - mass_y) < self.mass_radius:
                    self.dragging = True
                    self.v = 0
                elif reset_rect.collidepoint(event.pos):
                    self.reset()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

            self.speed_slider.handle_event(event)
            self.resistance_slider.handle_event(event)

        if self.dragging:
            self.pos = mouse_x - self.anchor[0] - self.rest_length

    def update(self, dt):
        dt *= self.speed_slider.value
        if not self.dragging:
            c = self.resistance_slider.value
            a = (-self.k * self.pos - c * self.v) / self.m
            self.v += a * dt
            self.pos += self.v * dt

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Spring anchor and mass
        pygame.draw.rect(self.screen, (120, 120, 120), (self.anchor[0] - 10, self.anchor[1] - 40, 20, 80))
        mass_x = int(self.anchor[0] + self.rest_length + self.pos)
        mass_y = self.anchor[1]
        pygame.draw.line(self.screen, (0, 0, 0), self.anchor, (mass_x, mass_y), 3)
        pygame.draw.circle(self.screen, (0, 100, 200), (mass_x, mass_y), self.mass_radius)

        # UI elements
        self.speed_slider.draw(self.screen)
        self.resistance_slider.draw(self.screen)

        # Reset button
        reset_rect = pygame.Rect(700, 10, 80, 30)
        pygame.draw.rect(self.screen, (220, 100, 100), reset_rect)
        text = self.font.render("Reset", True, (255, 255, 255))
        self.screen.blit(text, (reset_rect.x + 12, reset_rect.y + 5))

        msg = self.font.render("Press ESC to return to the menu.", True, (0, 0, 0))
        self.screen.blit(msg, (10, 10))

        pygame.display.flip()
