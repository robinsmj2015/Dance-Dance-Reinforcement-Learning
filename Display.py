import matplotlib.pyplot as plt
import numpy as np
import pygame
from Arrow import Arrow
import sys


class Display:
    """Used for displaying the agent interacting in the DDRL environment"""

    def __init__(self):
        pass

    @staticmethod
    def display_results(total_train_rewards, total_infer_rewards, losses, epoch):
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3)
        ax0.plot(np.arange(len(total_train_rewards)), total_train_rewards, color="blue", label="Training rewards")
        ax0.set(xlabel="episodes", ylabel="total rewards", title="Train Rewards")
        ax1.plot(np.arange(len(total_infer_rewards)), total_infer_rewards, color="green", label="Inference rewards")
        ax1.set(xlabel="episodes", ylabel="total rewards", title="Inference Reward")
        ax2.plot(np.arange(len(losses)), losses, color="orange", label="Training loss")
        ax2.set(xlabel="episodes", ylabel="Huber Loss", title="Huber Loss")
        ax0.legend()
        ax1.legend()
        ax2.legend()
        fig.suptitle("DDRL (epoch {0})".format(epoch))
        plt.tight_layout()
        # fig.canvas.manager.full_screen_toggle()
        plt.show()

    def basic_display(self, screen, color):
        # direction of screen
        # _, U, D, L, R, UD, LR
        print("--------------------------------")
        conv_dict = {0: "_", 1: "^", 2: "v", 3: "<", 4: ">", 5: "^v", 6: "<>"}
        print(self.color_helper(color) + conv_dict.get(screen[0]) + self.color_helper(""))
        for i in range(1, len(screen)):
            to_print = self.color_helper("B") + conv_dict.get(screen[i]) + self.color_helper("")
            print(to_print)

    @staticmethod
    def display_env(arrows_generated, actions_taken):
        arrows = []
        arrow_x = 20 // 2
        arrow_y = -3
        arrows_dict = {0: "blank", 1: "up", 2: "down", 3: "left", 4: "right", 5: "updown", 6: "leftright"}
        for i in range(len(actions_taken)):
            arrow_type = arrows_dict.get(arrows_generated[i])
            arrows.append(Arrow(arrow_type, arrow_x, arrow_y, 50, 20))

        pygame.init()
        window = pygame.display.set_mode((500, 500))

        white = (255, 255, 255)
        black = (0, 0, 0)

        run = True
        clock = pygame.time.Clock()
        #keep track of which arrow is in first position
        first = 0
        index = 0
        count = 0
        while run:
            window.fill(white)
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            sublist = arrows[first:index + 1]
            for a in sublist:
                if a.points:
                    points = a.update()
                    for p in points:
                        pygame.draw.polygon(window, black, p)
            pygame.display.flip()
            count += 1
            if count == 30:
                index += 1
                count = 0
            if arrows[first].arrow_y >= 450:
                first += 1
            if index >= len(arrows):
                run = False

        pygame.quit()
        sys.exit()

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
