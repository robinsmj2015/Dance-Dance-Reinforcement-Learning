import numpy as np


class State:
    '''
    State represented as [LF, RF, 5 arrows]
    '''
    def __init__(self, lf, rf, screen):
        self.screen = screen  # which arrows / blanks are on the screen for the agent to see
        self.lf = lf  # left foot position
        self.rf = rf  # right foot position

    # returns the state as an array of length 5
    def get_array(self):
        array = np.array([self.lf, self.rf] + self.screen)
        return array.copy()


