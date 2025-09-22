import pygame
from menu import Menu
from problems.pendulum import PendulumSim

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Physics Simulator")

    menu = Menu(screen)
    running = True

    while running:
        choice = menu.run()
        if choice == "pendulum":
            sim = PendulumSim(screen)
            sim.run()
        elif choice == "quit":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
