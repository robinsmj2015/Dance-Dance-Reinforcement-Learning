import matplotlib.pyplot as plt
import numpy as np
import pygame
from Arrow import Arrow


class Display:
    """Used for displaying the agent interacting in the DDRL environment"""

    def __init__(self):
        pass

    @staticmethod
    def display_results(total_train_rewards, total_infer_rewards, losses, epoch, epsilon, epsilon_drop, softmax):
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3)
        train_to_plot = []
        loss_to_plot = []
        # averaging over 100 episodes for better display
        for i in range(len(total_train_rewards) // 100):
            train_to_plot.append(np.mean(total_train_rewards[i:i + 100]))
            loss_to_plot.append(np.mean(losses[i: i + 100]))

        # the plots
        ax0.plot(np.arange(len(train_to_plot)), train_to_plot, color="blue", label="Training rewards")
        ax0.set(xlabel="episodes (in hundreds)", ylabel="total rewards", title="Train Rewards (Average {0:.1f})".format(np.mean(train_to_plot)))
        ax1.plot(np.arange(len(total_infer_rewards)), total_infer_rewards, color="green", label="Inference rewards")
        ax1.set(xlabel="episodes", ylabel="total rewards", title="Inference Reward (Average {0:.1f})".format(np.mean(total_infer_rewards)))
        ax2.plot(np.arange(len(loss_to_plot)), loss_to_plot, color="orange", label="Training loss")
        ax2.set(xlabel="episodes (in hundreds)", ylabel="Huber Loss", title="Huber Loss")
        ax0.legend()
        ax1.legend()
        ax2.legend()
        fig.suptitle("DDRL (epoch {0}): start_epsilon={1}, epsilon_drop={2}, softmax={3}".format(epoch, epsilon, epsilon_drop, softmax))
        plt.tight_layout()
        plt.show()

    @staticmethod
    def check_action(action, arrow):
        # only maps valid arrow combinations
        action_to_arrow_mapping = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1, (2, 0): 2, (0, 2): 2, (2, 2): 2,
                                   (3, 0): 3, (0, 3): 4,
                                   (1, 2): 5, (2, 1): 5, (3, 3): 6}

        # could be none if invalid arrow combination was picked (ex: [2,3])
        action_to_arrow = action_to_arrow_mapping.get(action)
        if action_to_arrow == arrow:
            return True
        return False

    def display_env(self, arrows_generated, actions_taken):
        # initialize the colors
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        green = (0, 255, 0)

        arrows = []
        arrow_x = 10
        arrows_dict = {0: "blank", 1: "up", 2: "down", 3: "left", 4: "right", 5: "updown", 6: "leftright"}
        for i in range(len(actions_taken)):
            arrow_type = arrows_dict.get(arrows_generated[i])
            if arrow_type == "blank":
                arrows.append(Arrow(arrow_type, arrow_x, i * -100, 50, 20, white))
            else:
                arrows.append(Arrow(arrow_type, arrow_x, i * -100, 50, 20, black))

        pygame.init()
        window = pygame.display.set_mode((500, 500))

        run = True
        clock = pygame.time.Clock()
        # keep track of which arrow is in first position
        first = 0
        index = 0
        while run:
            window.fill(white)
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # check if arrow is correct
            if arrows[first].arrow_y >= 450:
                correct = self.check_action(tuple(actions_taken[first]), arrows_generated[first])
                if correct:
                    arrows[first].color = green
                else:
                    arrows[first].color = red
            #  update arrow positions and draw them on screen
            for a in arrows:
                points = a.update()
                if a.points:
                    for p in points:
                        pygame.draw.polygon(window, a.color, p)
            pygame.display.flip()
            index += 1
            if arrows[first].arrow_y >= 475:
                first += 1
            if arrows[len(arrows) - 1].arrow_y >= 475:
                run = False

        pygame.quit()

    @staticmethod
    def color_helper(color_code=""):
        if color_code == "B":
            return "\033[0;34m"
        elif color_code == "R":
            return "\033[0;31m"
        elif color_code == "G":
            return "\033[0;32m"
        else:
            return "\033[0m"
