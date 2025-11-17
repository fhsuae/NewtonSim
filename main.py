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

    try:
        icon = pygame.image.load("assets/icons/NewtonSim Icon.jpg")
        pygame.display.set_icon(icon)
    except Exception as e:
        print(f"Warning: Could not load icon ({e})")

    # Set fullscreen display mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Physics Simulator")
    screen_rect = screen.get_rect()

    menu = Menu(screen)
    clock = pygame.time.Clock()
    running = True

    state = "menu"
    current_choice = None
    question_window = None
    explanation_window = None
    simulation = None

    question_result = None

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC quits simulation and goes back to menu if not already there
                    if state != "menu":
                        state = "menu"
                        simulation = None
                        question_window = None
                        explanation_window = None
                    else:
                        running = False

        # Always draw menu background first so it stays in the background
        menu.draw_background()

        if state == "menu":
            menu.update(events)
            menu.draw()
            pygame.display.flip()

            if menu.clicked_button:
                current_choice = menu.clicked_button
                menu.clicked_button = None

                if current_choice == "quit":
                    running = False
                    continue

                # Set question, correct answer, explanation, hints depending on choice
                if current_choice == "pendulum":
                    question = "What is the potential energy of a 1kg pendulum at 45° with length 2m?"
                    correct = 9.81 * 1 * 2 * (1 - math.cos(math.pi / 4))
                    explanation = (
                        "Potential energy of a pendulum at height h is PE = m * g * h. "
                        "Here, h = L * (1 - cos(theta)), m = 1kg, L = 2m, g = 9.81 m/s², "
                        "theta = 45°. Substituting values gives PE ≈ 1 * 9.81 * 2 * (1 - cos(π/4))."
                    )
                    hints = [
                        "Potential energy depends on height relative to lowest point.",
                        "Height can be found using h = L * (1 - cos(theta)).",
                        "Use g = 9.81 m/s² and m = 1kg."
                    ]

                elif current_choice == "spring":
                    question = "What is the potential energy of a spring stretched by 0.3m with k=20N/m?"
                    correct = 0.5 * 20 * (0.3 ** 2)
                    explanation = (
                        "Potential energy of a spring is PE = 1/2 * k * x². "
                        "Here, k = 20 N/m and x = 0.3 m. Substituting gives PE = 0.5 * 20 * (0.3²)."
                    )
                    hints = [
                        "Potential energy formula involves the spring constant and displacement squared.",
                        "k is given as 20 N/m, and x = 0.3 m.",
                        "Calculate 0.5 * k * x^2."
                    ]

                elif current_choice == "wave":
                    question = "If a wave has amplitude 50, what is its maximum displacement?"
                    correct = 50
                    explanation = (
                        "The maximum displacement of a wave equals its amplitude. "
                        "So maximum displacement = 50."
                    )
                    hints = [
                        "Maximum displacement equals the amplitude of the wave.",
                        "Here amplitude is given as 50."
                    ]

                else:
                    current_choice = None
                    continue

                question_window = QuestionWindow(question, correct, screen, hints)
                explanation_window = ExplanationWindow(explanation, screen)
                state = "question"

        elif state == "question":
            if question_window:
                question_result = question_window.run()

                if question_result["closed"]:
                    state = "menu"
                    question_window = None
                    continue

                if question_result["correct"]:
                    state = "simulation"
                else:
                    if question_result["attempts_exceeded"]:
                        state = "explanation"
                    else:
                        state = "question"

        elif state == "explanation":
            if explanation_window:
                exited_normally = explanation_window.run()
                if not exited_normally:
                    state = "menu"
                    explanation_window = None
                else:
                    state = "simulation"

        elif state == "simulation":
            if simulation is None:
                if current_choice == "pendulum":
                    simulation = PendulumSim(screen)
                elif current_choice == "spring":
                    simulation = SpringSim(screen)
                elif current_choice == "wave":
                    simulation = WaveSim(screen)
                else:
                    simulation = None

            if simulation:
                continue_sim = simulation.run()
                if not continue_sim:
                    simulation = None
                    state = "menu"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
