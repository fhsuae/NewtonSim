import pygame
import math

class PendulumSim:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.origin = (400, 100)
        self.length = 200
        self.angle = math.pi / 4
        self.omega = 0
        self.alpha = 0
        self.g = 9.81

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        self.alpha = -(self.g / self.length) * math.sin(self.angle)
        self.omega += self.alpha
        self.angle += self.omega * 0.05  # step size

    def draw(self):
        self.screen.fill((255, 255, 255))

        bob_x = self.origin[0] + self.length * math.sin(self.angle)
        bob_y = self.origin[1] + self.length * math.cos(self.angle)
        pygame.draw.line(self.screen, (0, 0, 0), self.origin, (bob_x, bob_y), 2)
        pygame.draw.circle(self.screen, (200, 0, 0), (int(bob_x), int(bob_y)), 20)
        pygame.display.flip()
