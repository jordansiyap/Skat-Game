import numpy as np
from model import Model
import random
import os
from game_environment import SkatGameEnvironment
from tensorflow.keras.models import load_model #if this import doesn't work use: from tensorflow.python.keras.models import load_model
from collections import deque
from plotter import update

class AIAgent:
    def __init__(self, state_size, action_size, model_path="best_model.h5"):
        #self.model = Model(state_size, action_size)

        # Load the model if it exists, otherwise create a new one
        if os.path.exists(model_path):
            print(f"Loading model from {model_path}...")
            self.model = load_model(model_path)
        else:
            print("Creating a new model...")
            self.model = Model(state_size, action_size)

        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 1.5  # Exploration rate
        self.epsilon_decay = 0.9999
        self.epsilon_min = 0.001
        self.memory = deque(maxlen=100000)  # Replay buffer
        self.batch_size = 100  # Batch size for training

    def act(self, state, hand):
        print("We Enter act") 
        """
        Selects an action using an epsilon-greedy policy.
        Returns the selected card and its index in the hand.
        """
        if np.random.rand() <= self.epsilon:
            # Explore: random legal move
            action_index = random.randint(0, 9)  # 9 == len(hand) - 1
            return action_index
        else:
            # Exploit: best predicted move
            print("We enter else in act()")
            state_vector = self._state_to_vector(state)
            action_probs = self.model.predict(state_vector)
            action_index = np.argmax(action_probs)
            #print("action index: ", action_index, "  --- hand_length: ", len(hand))

            print("We Quit act") 
            return action_index

    def train(self, state, action_index, reward, next_state, done):
        """ 
        train short memory

        """
        print("We Enter Train") 
        state_vector = self._state_to_vector(state)
        next_state_vector = self._state_to_vector(next_state)
        #print(state_vector)
        #print(state)
        #print(next_state)
        #print(len(state_vector))
        target = reward + 0.95 * np.max(self.model.predict(next_state_vector)) * (not done)
        target_f = self.model.predict(state_vector)
        target_f[0][action_index] = target
        self.model.train(state_vector, target_f)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        print("We Quit Train")     


    def remember(self, state, action_index, reward, next_state, done):
        """
        Stores experience in replay buffer.
        """
        self.memory.append((state, action_index, reward, next_state, done))

    def replay(self, batch_size):
        """
        Trains the model using experience replay.
        """
        print("We Enter replay")
        if len(self.memory) < batch_size:
            return  # Not enough experiences to train

        # Sample a minibatch from the replay buffer
        minibatch = random.sample(self.memory, batch_size)

        # Prepare training data
        states = np.zeros((batch_size, self.state_size))
        targets = np.zeros((batch_size, self.action_size))

        for i, (state, action_index, reward, next_state, done) in enumerate(minibatch):
            state_vector = self._state_to_vector(state)
            next_state_vector = self._state_to_vector(next_state)

            # Predict the Q-values for the current state
            target = self.model.predict(state_vector)

            # Update the target Q-value for the selected action
            if done:
                target[0][action_index] = reward
            else:
                target[0][action_index] = reward + 0.95 * np.max(self.model.predict(next_state_vector))

            states[i] = state_vector
            targets[i] = target

        # Train the model
        self.model.train(states, targets)

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        print("We Quit Replay")    

    def _state_to_vector(self, state):
        """
        Combines all state encodings into a single representation.
        """
        hand_encoding = self._encode_hand(state["hand"])
        open_round_encoding = self._encode_open_round(state["open_round"])
        betting_order_encoding = self._encode_betting_order(state["open_round"]["order"])
        gamemode_encoding = self._encode_gamemode(state["gamemode"])

        return np.concatenate(
            [hand_encoding, open_round_encoding, betting_order_encoding, gamemode_encoding]
        ).reshape(1, -1)
    

    def _encode_hand(self, hand):
        """
        Encodes the hand into a fixed-size representation.  32 bits
        """
        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]
        encoding = np.zeros((len(suits), len(values)))

        for card in hand:
            suit_index = suits.index(card["suit"])
            value_index = values.index(card["value"])
            encoding[suit_index][value_index] = 1

        return encoding.flatten()

    def _encode_open_round(self, open_round):
        """
        Encodes the open_round into a fixed-size representation. 32 bits
        """
        encoding = np.zeros(32)  # Max possible cards in a round

        for card in open_round["cards"].values():
            suits = ["clubs", "spades", "hearts", "diamonds"]
            values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]
            suit_index = suits.index(card["suit"])
            value_index = values.index(card["value"])
            encoding[suit_index * 8 + value_index] = 1

        return encoding
    
    def _encode_gamemode(self, gamemode):
        """
        Encodes the gamemode into a fixed-size representation. 6 bits
        """
        encoding = np.zeros(6)
        gamemodes = ["Grand", "Nullspiel", "Kreuz", "Pik", "Herz", "Karo"]
        encoding[gamemodes.index(gamemode["name"])] = 1
        return encoding
    
    def _encode_betting_order(self, order):
        """
        Encodes the betting order into a one-hot representation for all 6 possible arrangements. 6 bits
        """
        only_possible_orders = [
            ["player1", "player2", "player3"],
            ["player1", "player3", "player2"],
            ["player2", "player1", "player3"],
            ["player2", "player3", "player1"],
            ["player3", "player1", "player2"],
            ["player3", "player2", "player1"],
        ]
        encoding = np.zeros(len(only_possible_orders))
        for i, possible_order in enumerate(only_possible_orders):
            if order == possible_order:
                encoding[i] = 1
                break
        return encoding
    
    def save_model(self):
        """
        Saves the current model to the specified path.
        """
        self.model.model.save("best_model.h5")

if __name__ == "__main__":
    env = SkatGameEnvironment()
    state_size = 76
    action_size = 10
    total_not_legal_moves_since_training_start = 0
    plot_not_legal_moves = []  # Stores the number of not legal moves per game
    plot_mean_not_legal_moves = [] # store mean not legal moves
    plot_winning_rounds = []  # Stores the number of winning rounds per game (always empty for this easy ai)
    #games = []  # Stores the game number (x-axis)
    agent = AIAgent(state_size, action_size)

    

    for episode in range(200000):
        state = env.reset()
        done = False
        count_total_moves_in_this_game = 0  # Counter for not_legal moves in this game
        mean_not_legal_moves = 0
        winning_rounds_count = 0  # Counter for winning rounds in this game

        while not done:
            # AI selects an action
            action_index = agent.act(state, state["hand"])

            # Perform the action in the environment
            next_state, reward, done = env.step(action_index)
            
            # Update counters based on the reward
            count_total_moves_in_this_game += 1
            
            # Train short memory
            agent.train(state, action_index, reward, next_state, done)

            # Store this experience in the replay buffer
            agent.remember(state, action_index, reward, next_state, done)

            # Move to the next state
            state = next_state

        # Train the model using experience replay if game is done 
        agent.replay(agent.batch_size)    

        
        count_not_legal_moves_in_this_game = count_total_moves_in_this_game - 10

        #calculate the new mean not legal moves
        total_not_legal_moves_since_training_start += count_not_legal_moves_in_this_game
        mean_not_legal_moves = total_not_legal_moves_since_training_start / (episode + 1)


        # Update the plot after each game
        plot_not_legal_moves.append(count_not_legal_moves_in_this_game)
        plot_mean_not_legal_moves.append(mean_not_legal_moves)
        ##plot_winning_rounds.append(winning_rounds_count)


        update(plot_not_legal_moves, plot_mean_not_legal_moves, plot_winning_rounds)

        print(f"Episode {episode + 1}, Epsilon: {agent.epsilon}")
