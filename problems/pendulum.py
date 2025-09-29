import pygame
import math

class Slider:
    def __init__(self, x, y, width, min_val=0.1, max_val=2.0, initial=1.0):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.handle_pos = x + (initial - min_val) / (max_val - min_val) * width
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        pygame.draw.circle(screen, (50, 50, 200), (int(self.handle_pos), self.rect.centery), 10)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(self.handle_pos-10, self.rect.centery-10, 20, 20).collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_pos = max(self.rect.left, min(self.rect.right, event.pos[0]))
            t = (self.handle_pos - self.rect.left) / self.rect.width
            self.value = self.min_val + t * (self.max_val - self.min_val)

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

        self.dragging = False
        self.font = pygame.font.SysFont(None, 30)
        self.speed_slider = Slider(50, 550, 200, 0.1, 2.0, 1.0)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
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

            self.speed_slider.handle_event(event)

        if self.dragging:
            dx = mouse_x - self.origin[0]
            dy = mouse_y - self.origin[1]
            self.angle = math.atan2(dx, dy)

    def update(self):
        speed = self.speed_slider.value
        if not self.dragging:
            self.alpha = -(self.g / self.length) * math.sin(self.angle)
            self.omega += self.alpha * 0.05 * speed
            self.angle += self.omega * 0.05 * speed

    def draw(self):
        self.screen.fill((255, 255, 255))
        bob_x = self.origin[0] + self.length * math.sin(self.angle)
        bob_y = self.origin[1] + self.length * math.cos(self.angle)
        pygame.draw.line(self.screen, (0, 0, 0), self.origin, (bob_x, bob_y), 2)
        pygame.draw.circle(self.screen, (200, 0, 0), (int(bob_x), int(bob_y)), 20)

        self.speed_slider.draw(self.screen)

        text_surface = self.font.render("Press ESC to return to menu", True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        speed_text = self.font.render(f"Speed: {self.speed_slider.value:.2f}", True, (0, 0, 0))
        self.screen.blit(speed_text, (300, 550))

        pygame.display.flip()
