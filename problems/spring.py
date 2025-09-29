import pygame

class SpringSim:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.anchor = (200, 300)
        self.rest_length = 150
        self.mass_radius = 20

        self.pos = 100.0
        self.v = 0.0
        self.k = 20.0
        self.m = 1.0

        self.dragging = False  # new
        self.font = pygame.font.SysFont("Arial", 18)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if abs(mouse_x - mass_x) < self.mass_radius and abs(mouse_y - mass_y) < self.mass_radius:
                    self.dragging = True
                    self.v = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        if self.dragging:
            self.pos = mouse_x - self.anchor[0] - self.rest_length

    def update(self, dt):
        if not self.dragging:
            a = -self.k * self.pos / self.m
            self.v += a * dt
            self.pos += self.v * dt

    def draw(self):
        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, (120, 120, 120),
                         (self.anchor[0] - 10, self.anchor[1] - 40, 20, 80))

        mass_x = int(self.anchor[0] + self.rest_length + self.pos)
        mass_y = self.anchor[1]
        pygame.draw.line(self.screen, (0, 0, 0), self.anchor, (mass_x, mass_y), 3)
        pygame.draw.circle(self.screen, (0, 100, 200), (mass_x, mass_y), self.mass_radius)

        text = self.font.render("Press ESC to return to the menu.", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()
