import pygame
from menu import Menu
from problems.pendulum import PendulumSim
from problems.spring import SpringSim
from problems.wave import WaveSim

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
        elif choice == "spring":
            sim = SpringSim(screen)
            sim.run()
        elif choice == "wave":
            sim = WaveSim()
            sim.run()
        elif choice == "quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
