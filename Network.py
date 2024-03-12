import numpy as np
import torch
from torch.nn import Module
from torch.nn import Linear
import torch.nn.functional as F


"The network for both policy and target networks"
class Network(Module):
    def __init__(self, input_size, num_actions):
        super(Network, self).__init__()
        # the FC layers
        self.fc0 = Linear(input_size, 32)
        self.fc1 = Linear(32, 64)
        self.fc2 = Linear(64, 128)
        self.fc3 = Linear(128, num_actions)
        # Adam optimizer
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001, amsgrad=True)

    # forward propagation with ReLU activation
    def forward(self, x):
        if type(x) is np.ndarray:
            x = torch.as_tensor(x.copy(), dtype=torch.float)

        for layer in [self.fc0, self.fc1, self.fc2]:
            x = F.relu(layer(x))
        return self.fc3(x)


