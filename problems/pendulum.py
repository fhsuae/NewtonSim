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

        self.dragging = False  # new
        self.font = pygame.font.SysFont(None, 30)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bob_x = self.origin[0] + self.length * math.sin(self.angle)
        bob_y = self.origin[1] + self.length * math.cos(self.angle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if math.hypot(mouse_x - bob_x, mouse_y - bob_y) < 20:
                    self.dragging = True
                    self.omega = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        if self.dragging:
            dx = mouse_x - self.origin[0]
            dy = mouse_y - self.origin[1]
            self.angle = math.atan2(dx, dy)

    def update(self):
        if not self.dragging:  # only simulate if not dragging
            self.alpha = -(self.g / self.length) * math.sin(self.angle)
            self.omega += self.alpha * 0.05
            self.angle += self.omega * 0.05

    def draw(self):
        self.screen.fill((255, 255, 255))

        bob_x = self.origin[0] + self.length * math.sin(self.angle)
        bob_y = self.origin[1] + self.length * math.cos(self.angle)
        pygame.draw.line(self.screen, (0, 0, 0), self.origin, (bob_x, bob_y), 2)
        pygame.draw.circle(self.screen, (200, 0, 0), (int(bob_x), int(bob_y)), 20)

        text_surface = self.font.render("Press ESC to return to menu", True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()
