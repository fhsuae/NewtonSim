import pygame
import math

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.label = label
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            ratio = (event.pos[0] - self.rect.x) / self.rect.w
            self.value = max(self.min_val, min(self.max_val, self.min_val + ratio * (self.max_val - self.min_val)))

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        pos_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
        pygame.draw.circle(screen, (255, 100, 100), (pos_x, self.rect.centery), 10)
        font = pygame.font.SysFont(None, 24)
        screen.blit(font.render(f"{self.label}: {self.value:.2f}", True, (0, 0, 0)), (self.rect.x, self.rect.y - 25))


class WaveSim:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        self.time = 0
        self.k = 0.05
        self.paused = False

        # Sliders
        self.speed_slider = Slider(50, 520, 200, 20, 0.1, 2.0, 1.0, "Speed")
        self.amp_slider = Slider(50, 550, 200, 20, 10, 100, 50, "Amplitude")

        # Pause and Reset buttons
        self.pause_rect = pygame.Rect(650, 10, 100, 30)
        self.reset_rect = pygame.Rect(760, 10, 80, 30)

        self.running = True  # Track running state

    def run(self):
        dt = self.clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_rect.collidepoint(event.pos):
                    self.paused = not self.paused
                elif self.reset_rect.collidepoint(event.pos):
                    self.time = 0

            self.speed_slider.handle_event(event)
            self.amp_slider.handle_event(event)

        if not self.paused:
            self.update(dt)
        self.draw()
        return self.running

    def update(self, dt):
        self.time += dt * self.speed_slider.value * 5

    def draw(self):
        self.screen.fill((255, 255, 255))
        mid_y = 300
        amp = self.amp_slider.value

        points = [(x, mid_y + amp * math.sin(self.k * x - self.time)) for x in range(0, 800, 5)]
        pygame.draw.lines(self.screen, (0, 0, 255), False, points, 3)

        self.speed_slider.draw(self.screen)
        self.amp_slider.draw(self.screen)

        # Draw pause button
        pygame.draw.rect(self.screen, (100, 220, 100), self.pause_rect)
        self.screen.blit(self.font.render("Pause" if not self.paused else "Play", True, (255, 255, 255)),
                         (self.pause_rect.x + 20, self.pause_rect.y + 5))

        # Draw reset button
        pygame.draw.rect(self.screen, (220, 100, 100), self.reset_rect)
        reset_text = self.font.render("Reset", True, (255, 255, 255))
        self.screen.blit(reset_text, (self.reset_rect.x + 10, self.reset_rect.y + 5))

        self.screen.blit(self.font.render("Press ESC to return to the menu.", True, (0, 0, 0)), (10, 10))
        pygame.display.flip()
