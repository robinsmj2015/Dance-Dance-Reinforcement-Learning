from collections import deque
import numpy as np


class State:
    '''
    State represented as [LF, RF, 5 arrows]
    '''
    def __init__(self, lf, rf, screen):
        self.screen = screen
        self.lf = lf
        self.rf = rf

    def get_array(self):
        array = np.array([self.lf, self.rf] + self.screen)
        return array.copy()


