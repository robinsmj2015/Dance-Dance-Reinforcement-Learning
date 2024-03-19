import numpy as np
import torch
from torch.nn import Module
from torch.nn import Linear
import torch.nn.functional as F


class Network(Module):
    """The network for both policy and target networks"""
    def __init__(self, input_size, num_actions):
        super(Network, self).__init__()
        # the FC layers
        self.fc0 = Linear(input_size, 16)
        self.fc1 = Linear(16, 32)
        self.fc2 = Linear(32, num_actions)
        # Adam optimizer
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001, amsgrad=True)

    # forward propagation with ReLU activation
    def forward(self, x):
        # convert inputs to tensor if they are not already
        if type(x) is np.ndarray:
            x = torch.as_tensor(x.copy(), dtype=torch.float)
        for layer in [self.fc0, self.fc1]:
            x = F.relu(layer(x))
        return self.fc2(x)



