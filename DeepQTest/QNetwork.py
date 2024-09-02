import gym
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

# Initialize the environment
env = gym.make('CartPole-v1')

# Define the Q-Network
class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Hyperparameters
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
learning_rate = 0.001
gamma = 0.99
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
batch_size = 64
memory_size = 1000000

# Initialize Q-Network and optimizer
q_network = QNetwork(state_size, action_size)
optimizer = optim.Adam(q_network.parameters(), lr=learning_rate)

# Replay memory
memory = deque(maxlen=memory_size)

def select_action(state, epsilon):
    if random.random() <= epsilon:
        return env.action_space.sample()  # Explore
    else:
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = q_network(state)
        return np.argmax(q_values.numpy())  # Exploit

def optimize_model():
    if len(memory) < batch_size:
        return

    # Sample a random mini-batch of transitions
    mini_batch = random.sample(memory, batch_size)

    states, actions, rewards, next_states, dones = zip(*mini_batch)

    states = torch.FloatTensor(states)
    actions = torch.LongTensor(actions).unsqueeze(1)
    rewards = torch.FloatTensor(rewards)
    next_states = torch.FloatTensor(next_states)
    dones = torch.FloatTensor(dones)

    # Compute Q-values for current states
    q_values = q_network(states).gather(1, actions).squeeze()

    # Compute Q-values for next states
    with torch.no_grad():
        next_q_values = q_network(next_states).max(1)[0]

    # Compute the target Q-values
    targets = rewards + (gamma * next_q_values * (1 - dones))

    # Compute the loss
    loss = nn.MSELoss()(q_values, targets)

    # Perform a gradient descent step
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

num_episodes = 1000
target_update = 10  # Update the target network every 10 episodes

# Initialize the target network
target_network = QNetwork(state_size, action_size)
target_network.load_state_dict(q_network.state_dict())

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0

    for t in range(200):  # Limit each episode to 200 steps
        action = select_action(state, epsilon)
        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        # Store the transition in replay memory
        memory.append((state, action, reward, next_state, done))

        state = next_state

        optimize_model()

        if done:
            break

    # Reduce exploration rate
    epsilon = max(epsilon_min, epsilon_decay * epsilon)

    # Print episode statistics
    print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

    # Update the target network periodically
    if (episode + 1) % target_update == 0:
        target_network.load_state_dict(q_network.state_dict())
