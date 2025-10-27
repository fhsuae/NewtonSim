import pygame
from menu import Menu
from problems.pendulum import PendulumSim
from problems.spring import SpringSim
from problems.wave import WaveSim
from problems.question_window import QuestionWindow
import math


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Physics Simulator")

    menu = Menu(screen)
    running = True

    while running:
        choice = menu.run()

        if choice == "pendulum":
            question = "What is the potential energy of a 1kg pendulum at 45° with length 2m?"
            correct = 9.81 * 1 * 2 * (1 - math.cos(math.pi / 4))
            q = QuestionWindow(screen, question, correct)
            if q.run():
                sim = PendulumSim(screen)
                sim.run()

        elif choice == "spring":
            question = "What is the potential energy of a spring stretched by 0.3m with k=20N/m?"
            correct = 0.5 * 20 * (0.3 ** 2)
            q = QuestionWindow(screen, question, correct)
            if q.run():
                sim = SpringSim(screen)
                sim.run()

        elif choice == "wave":
            question = "If a wave has amplitude 50, what is its maximum displacement?"
            correct = 50
            q = QuestionWindow(screen, question, correct)
            if q.run():
                sim = WaveSim(screen)
                sim.run()

        elif choice == "quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
