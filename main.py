from Display import Display
from Agent import Agent
import numpy as np



# Hyperparameters
actions = np.arange(16)
memory_size = 10000

screen_length = 3
input_size = screen_length + 2
min_blanks = 1
target_update_period = 500
batch_size = 32
discount = 0.99
num_train_episodes = 100000
num_infer_episodes = 100
num_epochs = 1
epsilon = 1
epsilon_drop = 0.000005  # epsilon drop
early_stopping = -150
use_softmax = True


# Instances
display = Display()
agent = Agent(actions, memory_size, input_size, min_blanks, target_update_period, batch_size, discount, screen_length, early_stopping, use_softmax)

# The main loop... train then infer, then display our results!
for i in range(num_epochs):
    train_rewards, losses = agent.train_or_infer(is_training=True, num_episodes=num_train_episodes, epoch_num=i, epsilon=epsilon, epsilon_drop=epsilon_drop)
    infer_rewards, _ = agent.train_or_infer(is_training=False, num_episodes=num_infer_episodes, epoch_num=i)
    display.display_results(train_rewards, infer_rewards, losses, i)
    print("Inference scores:", infer_rewards)
    print("Mean inference score:", np.array(infer_rewards).mean())


# description:

# let's wait on holds
# let's wait on combos

# states:
# 5 screen positions of 5 moves (L, R, U, D, _),
# 4 positions for each foot (top, bottom, side, center),
# screen velocity - num moves between screen changes
# - I think minimum should be 2 or 3 and upper limit at 5 (maybe when starting off)'

# actions:
# left foot: U, D, S (sideways)
# right foot: U, D, S (sideways)
# no up

# rewards:
# +1 for each successful hit (including blanks)
# - 1 for miss






