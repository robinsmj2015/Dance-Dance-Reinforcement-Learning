import numpy as np
from State import State
import random


class Environment:
    '''
    states: 0 = center, 1 = up, 2 = down, 3 = side

    Actions: 0 = no-op, 1 = up, 2 = down, 3 = side
    '''

    def __init__(self, min_blanks, length):
        # actions mapped to the states that they start in and end in
        # any time start and end are the same it is a "not allowed" move
        self.actions = {1: {0: 1, 1: 1, 2: 0, 3: 3}, 2: {0: 2, 1: 0, 2: 2, 3: 3}, 3: {0: 3, 1: 1, 2: 2, 3: 0}}
        self.done = 0
        self.min_blanks = min_blanks
        self.length = length


        # keep track of which arrow we are at
        self.arrow_index = 0
        self.arrows = self.generate_song(100)
        self.screen = self.update_arrows()
        self.state = State(0, 0, self.screen)

        # total rewards
        self.total_rewards = 0

        # dictionary which stores the accurate foot position possibilities for each arrow
        self.arrow_dict = {0: [[0, 0]], 1: [[0, 1], [1, 0], [1, 1]], 2: [[0, 2], [2, 0], [2, 2]], 3: [[3, 0]],
                           4: [[0, 3]],
                           5: [[1, 2], [2, 1]], 6: [[3, 3]]}

    def update_state(self, action):
        '''
        updates the state (the position of the feet and the arrows on screen)
        based on the given action. also calculates the reward
        :param action: action to be taken in list form
        :return: next state, reward, done
        '''
        previous_state = self.state
        # derive new positions of feet based on the given action
        new_feet_state = self.take_action(action)

        # update the arrows for the new state (this may also change it to be a terminal state)
        updated_screen = self.update_arrows()
        # updating screen may change done, so reassign
        done = self.done

        updated_state = State(new_feet_state[0], new_feet_state[1], updated_screen)

        #calculate reward of the updated state
        reward = self.calc_reward(previous_state.get_array(), updated_state.get_array(), action)
        #add reward to total rewards
        self.total_rewards += reward

        self.state = updated_state
        return updated_state, reward, done

    def update_arrows(self):
        '''
        updates the arrows that are currently on the screen by increasing the index
        :return: list of arrows
        '''
        screen = self.arrows[self.arrow_index:self.arrow_index + self.length]
        self.arrow_index += 1
        if self.arrow_index >= 100:
            self.done = 1
        return screen

    def calc_reward(self, state, next_state, action_taken):
        '''
        plus one if it hits the arrow
        minus one for off board
        minus one for wrong hit
        no reward if nothing hit for a blank
        :param state:
        :param next_state:
        :param action_taken:
        :return: reward
        '''
        # target arrow will be the second arrow in state (next arrow that should be hit)
        target_arrow = state[3]

        # check if agent tried to move off board
        if (state[0] == next_state[0] and action_taken[0] != 0) or (state[1] == next_state[1] and action_taken[1] != 0):
            return -1

        # what the correct state should be depending on the given arrow
        target_states = self.arrow_dict.get(target_arrow)

        actual_state = list(next_state[:2])

        # check for blank
        if target_arrow == 0 and actual_state == [0, 0]:
            return 0

        # check if the actual states is one of the correct states
        for lst in target_states:
            if lst == actual_state:
                return 1

        return -1

    def generate_song(self, length):
        # 0 blank, U, D, L, R, UD, LR
        song = []
        while len(song) < (length):
            for j in range(self.min_blanks):
                move = 0
                song.append(move)
            move = np.random.choice(np.array([0, 1, 2, 3, 4, 5, 6]),
                                    p=np.array([0.08, 0.18, 0.18, 0.18, 0.18, 0.1, 0.1]))
            song.append(move)
        # pad end with 0's so that the last real arrow can reach the first position
        for i in range(5):
            song.append(0)
        return song

    def reset(self):
        '''
        reset the environment. generates new list of songss, reset state, set total rewards
        to 0
        :return:
        '''
        self.done = 0
        # initialize arrows (hardcoded for now)
        self.arrows = self.generate_song(100)
        # keep track of which arrow we are at
        self.arrow_index = 0
        self.arrows = self.generate_song(100)
        self.screen = self.update_arrows()
        self.state = State(0, 0, self.screen)
        # total rewards
        self.total_rewards = 0

    def take_action(self, action):
        '''
        :param action: action to be taken in list form
        :return: the new state that the feet are in given the action
        '''
        new_feet_state = []
        for i in range(len(action)):
            # no-op case
            if action[i] == 0:
                new_feet_state.append(self.state.get_array()[i])
            else:
                # left foot
                if i == 0:
                    prev_foot_state = self.state.lf
                    if type(prev_foot_state) == None:
                        print("error")
                    updated_foot_state = self.actions.get(action[i]).get(prev_foot_state)
                    new_feet_state.append(updated_foot_state)
                # right foot
                if i == 1:
                    prev_foot_state = self.state.rf
                    if type(prev_foot_state) == None:
                        print("error")
                    updated_foot_state = self.actions.get(action[i]).get(prev_foot_state)
                    new_feet_state.append(updated_foot_state)
        return new_feet_state

    def guide_explore(self, state):
        '''
        implement guided exploration
        :param state:
        :return: action to be taken in list form
        '''
        # store the current state that the feet are in
        lf = state[0]
        rf = state[1]

        #store the target arrow that we want to reach
        target_arrow = state[3]

        #store all the possible states that could be valid for the target arrow
        target_states = self.arrow_dict.get(target_arrow)

        #iterate through every possible good state (should only ever be 3 max)
        for s in target_states:
            action = []
            # start by checking if it should take no op
            lf_next = lf
            act_to_try = 0
            # iterate through all possible actions until left foot is in correct position
            while lf_next != s[0] and act_to_try < 3:
                act_to_try += 1
                lf_next = self.actions.get(act_to_try).get(lf)
            # add the action that matched to the list
            action.append(act_to_try)

            # start by checking if it should take no op
            rf_next = rf
            act_to_try = 0
            # iterate through all possible actions until right foot is in correct position
            while rf_next != s[1] and act_to_try < 3:
                act_to_try += 1
                rf_next = self.actions.get(act_to_try).get(rf)
            # add the action that matched to the list
            action.append(act_to_try)
            # return action if good state is reached
            if [lf_next, rf_next] == s:
                return action

        # if no good states can be reached, return random action
        return [random.randint(0, 3), random.randint(0, 3)]


