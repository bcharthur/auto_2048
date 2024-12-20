# rl_agent/qlearning_agent.py
import random

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_values = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state_key(self, state):
        return tuple(tuple(row) for row in state)

    def get_q(self, state, action):
        state_key = self.get_state_key(state)
        return self.q_values.get(state_key, {}).get(action, 0.0)

    def set_q(self, state, action, value):
        state_key = self.get_state_key(state)
        if state_key not in self.q_values:
            self.q_values[state_key] = {}
        self.q_values[state_key][action] = value

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values_actions = [(a, self.get_q(state, a)) for a in self.actions]
            max_q = max(q_values_actions, key=lambda x: x[1])[1]
            best_actions = [a for a, q in q_values_actions if q == max_q]
            return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        old_value = self.get_q(state, action)
        if done:
            target = reward
        else:
            next_values = [self.get_q(next_state, a) for a in self.actions]
            target = reward + self.gamma * max(next_values)
        new_value = old_value + self.alpha*(target - old_value)
        self.set_q(state, action, new_value)
