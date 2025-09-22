import pygame

class SpringSim:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True


        self.anchor = (200, 300)
        self.rest_length = 150.0
        self.mass_radius = 20


        self.pos = 0.0
        self.v = 0.0


        self.m = 1.0
        self.k = 20.0
        self.c = 0.8


        self.dragging = False
        self.grab_offset = 0.0


        self.font = pygame.font.SysFont("Arial", 18)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            if not self.dragging:
                self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    self.running = False
                elif event.key == pygame.K_r:

                    self.pos = 0.0
                    self.v = 0.0

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                mass_x = self.anchor[0] + self.rest_length + self.pos
                mass_y = self.anchor[1]

                if (mx - mass_x) ** 2 + (my - mass_y) ** 2 <= self.mass_radius ** 2:
                    self.dragging = True
                    self.grab_offset = mass_x - mx
                    self.v = 0.0

            elif event.type == pygame.MOUSEMOTION and self.dragging:
                mx, my = event.pos
                new_mass_x = mx + self.grab_offset

                self.pos = new_mass_x - (self.anchor[0] + self.rest_length)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
                self.dragging = False


    def update(self, dt):

        a = (-self.k * self.pos - self.c * self.v) / self.m

        self.v += a * dt
        self.pos += self.v * dt

    def draw(self):
        self.screen.fill((255, 255, 255))


        pygame.draw.rect(self.screen, (120, 120, 120),
                         (self.anchor[0] - 10, self.anchor[1] - 40, 20, 80))


        mass_x = int(self.anchor[0] + self.rest_length + self.pos)
        mass_y = int(self.anchor[1])


        pygame.draw.line(self.screen, (0, 0, 0), self.anchor, (mass_x, mass_y), 3)


        pygame.draw.circle(self.screen, (0, 100, 200), (mass_x, mass_y), self.mass_radius)


        lines = [
            "Drag the mass with left mouse button to set displacement.",
            "Press R to reset. Press ESC to return to the menu."
        ]
        for i, text in enumerate(lines):
            surf = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(surf, (10, 10 + i * 22))

        pygame.display.flip()
