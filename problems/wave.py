import pygame
import math

# Simple reusable slider class (same as before)
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
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.max_val, self.value))

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        pos_x = int(self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.w)
        pygame.draw.circle(screen, (255, 100, 100), (pos_x, self.rect.centery), 10)
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"{self.label}: {self.value:.2f}", True, (0, 0, 0))
        screen.blit(text, (self.rect.x, self.rect.y - 25))


class WaveSim:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Wave Motion Simulation")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)

        # Wave parameters
        self.time = 0
        self.k = 0.05   # wave number (controls wavelength)
        self.paused = False

        # Sliders
        self.speed_slider = Slider(50, 520, 200, 20, 0.1, 2.0, 1.0, "Speed")
        self.amp_slider = Slider(50, 550, 200, 20, 10, 100, 50, "Amplitude")

        # Pause button
        self.pause_rect = pygame.Rect(650, 10, 100, 30)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_rect.collidepoint(event.pos):
                        self.paused = not self.paused

                # Handle sliders
                self.speed_slider.handle_event(event)
                self.amp_slider.handle_event(event)

            if not self.paused:
                self.update(dt)
            self.draw()

    def update(self, dt):
        # Increase simulation time based on slider speed
        self.time += dt * self.speed_slider.value * 5

    def draw(self):
        self.screen.fill((255, 255, 255))
        mid_y = 300
        amp = self.amp_slider.value
        wavelength = 2 * math.pi / self.k

        # Draw wave
        points = []
        for x in range(0, 800, 5):
            y = mid_y + amp * math.sin(self.k * x - self.time)
            points.append((x, y))
        pygame.draw.lines(self.screen, (0, 0, 255), False, points, 3)

        # Sliders
        self.speed_slider.draw(self.screen)
        self.amp_slider.draw(self.screen)

        # Pause button
        pygame.draw.rect(self.screen, (100, 220, 100), self.pause_rect)
        pause_text = self.font.render("Pause" if not self.paused else "Play", True, (255, 255, 255))
        self.screen.blit(pause_text, (self.pause_rect.x + 20, self.pause_rect.y + 5))

        # Instructions
        text = self.font.render("Press ESC to return to the menu.", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()


if __name__ == "__main__":
    WaveSim().run()
