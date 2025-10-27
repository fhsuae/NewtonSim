### main.py
import pygame
from menu import Menu
from problems.pendulum import PendulumSim
from problems.spring import SpringSim
from problems.wave import WaveSim
from problems.question_window import QuestionWindow
from problems.explanation_window import ExplanationWindow
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
            explanation = (
                "Potential energy of a pendulum at height h is PE = m * g * h. "
                "Here, h = L * (1 - cos(theta)), m = 1kg, L = 2m, g = 9.81 m/s², "
                "theta = 45°. Substituting values gives PE ≈ 1 * 9.81 * 2 * (1 - cos(π/4))."
            )

            q = QuestionWindow(question, correct)
            if q.run():
                sim = PendulumSim(screen)
                sim.run()

                # Show explanation
                exp_win = ExplanationWindow(explanation, screen)
                exp_win.run()

        elif choice == "spring":
            question = "What is the potential energy of a spring stretched by 0.3m with k=20N/m?"
            correct = 0.5 * 20 * (0.3 ** 2)
            explanation = (
                "Potential energy of a spring is PE = 1/2 * k * x². "
                "Here, k = 20 N/m, x = 0.3 m. "
                "Substitute values: PE = 0.5 * 20 * (0.3)²."
            )

            q = QuestionWindow(question, correct)
            if q.run():
                sim = SpringSim(screen)
                sim.run()

                exp_win = ExplanationWindow(explanation, screen)
                exp_win.run()

        elif choice == "wave":
            question = "If a wave has amplitude 50, what is its maximum displacement?"
            correct = 50
            explanation = (
                "The maximum displacement of a wave is equal to its amplitude. "
                "Here, amplitude = 50, so maximum displacement = 50."
            )

            q = QuestionWindow(question, correct)
            if q.run():
                sim = WaveSim(screen)
                sim.run()

                exp_win = ExplanationWindow(explanation, screen)
                exp_win.run()

        elif choice == "quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
