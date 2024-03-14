from Display import Display
from Agent import Agent
import numpy as np


# Hyperparameters
actions = np.arange(16)  # the possible actions to take
memory_size = 10000  # number of transitions stored for experience replay
screen_length = 3  # how many arrows/ blanks appear on the screen for the agent
input_size = screen_length + 2  # the input size of the networks
min_blanks = 1  # the min number of blanks that must occur between each arrow
target_update_period = 500  # C
batch_size = 32
discount = 0.99  # discount factor
num_train_episodes = 20000
num_infer_episodes = 100
num_epochs = 1
epsilon = 0  # starting epsilon
epsilon_drop = 0  # epsilon drop per episode
use_softmax = True  # to use softmax draws rather than greedy choice
guided_exploration = True

# Instances
display = Display()
agent = Agent(actions, memory_size, input_size, min_blanks, target_update_period, batch_size, discount, screen_length, use_softmax, guided_exploration)

# The main loop... train then infer, then display our results!
for i in range(num_epochs):
    train_rewards, losses = agent.train_or_infer(is_training=True, num_episodes=num_train_episodes, epoch_num=i, epsilon=epsilon, epsilon_drop=epsilon_drop)
    infer_rewards, _ = agent.train_or_infer(is_training=False, num_episodes=num_infer_episodes, epoch_num=i)
    display.display_results(train_rewards, infer_rewards, losses, i, epsilon, epsilon_drop, use_softmax, guided_exploration)
    print("Inference scores:", infer_rewards)
    print("Mean inference score:", np.array(infer_rewards).mean())
