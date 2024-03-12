import random
import torch
from Network import Network
from collections import deque
from Environment import Environment
import numpy as np
from Transition import Transition
from Display import Display
from torchsummary import summary

class Agent:
    """Agent is trained to pick an optimal move in the DDRL environment.
    After training its dance skills will be tested in inference mode"""
    def __init__(self, actions, memory_size, input_size, min_blanks, target_update_period, batch_size, discount, screen_length):
        self.epsilon = None  # fraction of time that agent explores when training
        self.actions = actions  # actions the agent can choose from
        self.num_actions = len(actions)  # number of possible actions
        self.transitions = deque([], maxlen=memory_size)  # memory
        self.is_training = None  # True if the agent is training, False if in inference
        self.policy_net = Network(input_size, self.num_actions)  # instance of network
        self.target_net = Network(input_size, self.num_actions)  # instance of network
        self.tracking_num = 0  # tracking number - essentially step number but does not reset after each episode
        self.environment = Environment(min_blanks, screen_length)  # instance of the environment class
        self.display = Display()  # instance of display
        self.target_update_period = target_update_period  # C - update period of target network
        self.discount = discount  # discount factor
        self.batch_size = batch_size  # how many transitions are selected from the memory when training the policy net
        self.episode_rewards = []  # the rewards for each episode
        self.episode_losses = []  # the losses for each episode
        self.losses = 0  # cumulative losses (resets after every episode)
        self.loss_count = 0  # how many times the agent was trained
        self.print_summary(input_size)

    def print_summary(self, input_size):
        summary(self.policy_net, (1, input_size), device="cpu")

    # agent undergoes training or is used in inference mode - puts agent in the environment
    def train_or_infer(self, is_training, num_episodes, epoch_num, epsilon=0):
        """
        :param is_training:
        :param num_episodes:
        :param epsilon:
        :return: self.episode_rewards, self.episode_losses
        """
        self.is_training = is_training
        self.epsilon = epsilon
        self.episode_rewards = []
        self.episode_losses = []
        print("\n---------------------------- EPOCH {0} of {1} --------------------------------".format(epoch_num, "TRAINING" if is_training else "TESTING"))
        for i in range(num_episodes):
            done = False
            self.losses = 0
            self.loss_count = 0
            self.environment.reset()
            # for display purposes:
            actions_taken = []
            while not done:
                state, action, unnormalized_state = self.pick_action()
                action_list = self.action_to_list(action)
                actions_taken.append(action_list)
                next_state, reward, done = self.environment.update_state(action_list)

                if self.is_training:
                    # add to memory
                    self.add_transition(state, action, reward, self.normalize(next_state.get_array()), done)
                    # Target network update
                    if ((self.tracking_num + 1) % self.target_update_period) == 0:
                        self.update_target_network()
                    # Policy network update
                    if self.tracking_num > self.batch_size:
                        loss = self.update_policy_network()
                        self.losses += loss.detach()
                        self.loss_count += 1
                else:
                    pass
                    # Displays for inference mode
                    self.display.basic_display(unnormalized_state[2:], color="G" if reward == 1 else "R")
                self.tracking_num += 1

            # rewards for each episode
            self.episode_rewards.append(self.environment.total_rewards)
            #print("Episode: " + str(i))
            #print("Total Rewards: " + str(self.environment.total_rewards))
            # tracks the average loss
            if self.is_training:
                self.episode_losses.append(self.losses / self.loss_count)
            else:
                self.display.display_env(self.environment.arrows, actions_taken)
        return self.episode_rewards, self.episode_losses

    # determines agent's action
    def pick_action(self):
        """
        :return: state, action
        """
        state = self.environment.state.get_array().copy()
        unnormalized_state = self.environment.state.get_array().copy()
        state = self.normalize(state)
        # exploration or exploitation
        if np.random.rand() < self.epsilon:
            action = np.random.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.target_net.forward(state).detach()).item()
        return state, action, unnormalized_state

    @staticmethod
    def action_to_list(action):
        return [action // 4, action % 4]

    # adds a transition to the experience replay memory
    def add_transition(self, state, action, reward, next_state, done):
        self.transitions.append(Transition(state.copy(), action, reward, next_state.copy(), done))

    # updates the policy network
    def update_policy_network(self):
        """
        :return: loss
        """
        # samples the memory
        sel_transitions = random.sample(self.transitions, self.batch_size)
        info = [(sel_transition.s, sel_transition.a, sel_transition.r, sel_transition.s_prime, sel_transition.done) for
                sel_transition in sel_transitions]
        # separates each transition into its states, actions, rewards, next states and if it is a terminal state
        states, actions, rewards, state_primes, dones = zip(*info)
        # converting the above to tensors
        state_primes = torch.tensor(np.array(state_primes), requires_grad=False, dtype=torch.float)
        states = torch.tensor(np.array(states), dtype=torch.float, requires_grad=True)
        actions = torch.tensor(actions, requires_grad=False, dtype=torch.int64)
        rewards = np.array(rewards)

        # labels for the policy network
        with torch.no_grad():
            temp = np.zeros(self.batch_size)
            labels = np.max(np.array(self.target_net.forward(state_primes)), axis=1, out=temp) * self.discount + rewards
            labels = torch.tensor(labels, dtype=torch.float, requires_grad=False)

        # gets the agent's estimate of the Q value for only the actions it took
        init_outputs = self.policy_net.forward(states)
        outputs = torch.gather(init_outputs, index=actions.reshape((self.batch_size, 1)), dim=1)
        # modifies the labels (recall for terminal states the target is only the reward)
        for i, (done, reward) in enumerate(zip(dones, rewards)):
            labels[i] = reward if done else labels[i]

        # calculating the loss and back-propagating it
        loss_func = torch.nn.HuberLoss()
        self.policy_net.optimizer.zero_grad()
        loss = loss_func(outputs, torch.unsqueeze(labels, 1))
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.policy_net.optimizer.step()
        return loss

    # updates the target network by copying state dic of policy network
    def update_target_network(self):
        self.target_net.state_dict = self.policy_net.state_dict().copy()

    # normalizes the state to [0, 1]
    @staticmethod
    def normalize(state):
        """
        :param state: list
        :return: state
        """
        state = state.astype(float)

        num_foot_positions = 4
        num_screen_positions = 7
        #  normalize feet
        state[:2] = state[:2] / num_foot_positions
        # normalize screen
        state[2:] = state[2:] / num_screen_positions
        return state
