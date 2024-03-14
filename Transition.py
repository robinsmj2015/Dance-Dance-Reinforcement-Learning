
class Transition:
    '''a transition to be stored in the memory and used in experience replay'''
    def __init__(self, s, a, r, s_prime, done):
        self.s = s  # state
        self.a = a  # action
        self.r = r  # reward
        self.s_prime = s_prime  # next state
        self.done = done  # if the next state is terminal
