import random

class QLearningAgent:
    def __init__(self, actions):
        # The actions the agent can take (e.g., [0, 1, 2,3] for UP, DOWN, LEFT, RIGHT)
        self.actions = actions

        # The Q-Table: A dictionary mapping 'States' to list of 'Q-Values'
        self.q_table = {}

        # --- Hyperparameters (The duasl we turn to tune de AI's bran) ---
        self.alpha = 0.1    # Learning Rate: How much new info overides old info
        self.gamma = 0.9    # Discount Factor: Importance of future rewards

        # #xploration vs Exploitation (The Epsilon-Greedy strategy)
        self.epsilon = 1.0          # Starts at 100% exploration (totally random moves)
        self.epsilon_decay = 0.995  # How fast the agent stops the exploring and start exploiting
        self.epsilon_min = 0.01     # Will always explore at least 1% of the time

    def get_q_values(self, state):
        """ Returns the Q-Values for a given state. Initializes with 0.0 if unseen. """
        if state not in self.q_table:
            # Create a list of 0.0 for every possible action
            self.q_table[state] = [0.0 for _ in self.actions]
        return self.q_table[state]
    
    def choose__action(self, state):
        """ Decides whether to take a random action or the best known action. """
        # 1. EXPLORE: Take a random action to discover the map
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # 2. EXPLOIT: Use the Q-Table to pick the action with the highest value
        else:
            q_values = self.get_q_values(state)
            max_q = max(q_values)

            # If multiple action tie for the highest value, pick one randomly among
            best_actions = [i for i, q in enumerate(q_values) if q == max_q]
            return random.choice(best_actions)
        
    def learn(self, state, action_idx, reward, next_state):
        """ The Bellman Equation in Python. Updates the Q-Table. """
        q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)

        old_q_value = q_values[action_idx]
        next_max_q = max(next_q_values)

        # Calculate the new Q-value based on the reward and the best future prospect
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * next_max_q - old_q_value)

        # Update the table with the new knowledge
        self.q_table[state][action_idx] = new_q_value

        # Decay Epsilon: After learning, become slightly less random
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
