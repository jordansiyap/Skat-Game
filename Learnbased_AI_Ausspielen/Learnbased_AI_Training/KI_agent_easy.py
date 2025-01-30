import numpy as np
from model import Model
import random
import os
from game_environment_easy import SkatGameEnvironment
#from tensorflow.python.keras.models import load_model
from collections import deque
from utils import update
from utils import get_is_legal_move

class AIAgent:
    def __init__(self, state_size, action_size, model_path="RLeasyAI.weights.h5"):
        self.model = Model(state_size, action_size)

        if os.path.exists(model_path):
            print(f"Loading model from {model_path}...")
            self.model.model.load_weights(model_path)
        else:
            print("Creating a new model...")
            self.model = Model(state_size, action_size)

        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = 1.0
        self.epsilon_decay = 0.998
        self.epsilon_min = 0.01
        self.memory = deque(maxlen=100000)
        self.batch_size = 64  # Batch size for training

    def act(self, state):
        print("We Enter act")

        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]

        hand = state.get("hand")
        open_round = state.get("open_round")
        gamemode = state.get("gamemode")
        turn_order = state.get("turn_order")
    
        legal_actions_indexe = []

        for check_card in hand:

            suit_idx = suits.index(check_card["suit"])
            value_idx = values.index(check_card["value"])

            if not open_round.get("cards"):
                legal_actions_indexe.append(suit_idx * 8 + value_idx)
                continue

            card_to_try = {
                "open_round": open_round,
                "gamemode": gamemode,
                "check_card": check_card,
                "hand": hand 
            }

            is_legal = get_is_legal_move(card_to_try)
            if is_legal.get("status") == "true":
                legal_actions_indexe.append(suit_idx * 8 + value_idx)

        if np.random.rand() <= self.epsilon:
            action_index = random.choice(legal_actions_indexe) if legal_actions_indexe else 0

        else:
            
            state_vector = self._state_to_vector(state)
            action_probs = self.make_prediction(state)[0]
            masked_probs = np.full_like(action_probs, -np.inf)
            for idx in legal_actions_indexe:
                masked_probs[idx] = action_probs[idx]
            action_index = np.argmax(masked_probs)
    
        print("We Quit act") 
        return action_index

    def train(self, state, action_index, reward, next_state, done):
        """ 
        train short memory

        """
        state_vector = self._state_to_vector(state)
        target = reward + 0.95 * np.max(self.make_prediction(next_state)[0]) * (not done)
        target_f = self.make_prediction(state)
        target_f[0][action_index] = target
        self.model.train(state_vector, target_f)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay   


    def remember(self, state, action_index, reward, next_state, done):
        """
        Stores experience in replay buffer.
        """
        self.memory.append((state, action_index, reward, next_state, done))

    def replay(self, batch_size):
        """
        Trains the model using experience replay.
        """
        if len(self.memory) < batch_size:
            return  # Not enough experiences to train

        minibatch = random.sample(self.memory, batch_size)

        states = np.zeros((batch_size, self.state_size))
        targets = np.zeros((batch_size, self.action_size))

        for i, (state, action_index, reward, next_state, done) in enumerate(minibatch):
            state_vector = self._state_to_vector(state)
            target = self.make_prediction(state)

            if done:
                target[0][action_index] = reward
            else:
                target[0][action_index] = reward + 0.95 * np.max(self.make_prediction(next_state)[0])

            states[i] = state_vector
            targets[i] = target

        self.model.train(states, targets)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def make_prediction(self, state):


        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]

        hand = state.get("hand")
        open_round = state.get("open_round")
        gamemode = state.get("gamemode")
        turn_order = state.get("turn_order")
    
        legal_actions_indexe = []

        for check_card in hand:

            suit_idx = suits.index(check_card["suit"])
            value_idx = values.index(check_card["value"])

            if not open_round.get("cards"):
                legal_actions_indexe.append(suit_idx * 8 + value_idx)
                continue

            card_to_try = {
                "open_round": open_round,
                "gamemode": gamemode,
                "check_card": check_card,
                "hand": hand 
            }

            is_legal = get_is_legal_move(card_to_try)
            if is_legal.get("status") == "true":
                legal_actions_indexe.append(suit_idx * 8 + value_idx)

        state_vector = self._state_to_vector(state)
        action_probs = self.model.predict(state_vector)
        masked_probs = np.full_like(action_probs[0], -np.inf)
        for idx in legal_actions_indexe:
            masked_probs[idx] = action_probs[0][idx]

        action_probs[0] = masked_probs    
     
        return action_probs

    def _state_to_vector(self, state):
        """
        Combines all state encodings into a single representation.
        """
        hand_encoding = self._encode_hand(state["hand"])
        open_round_encoding = self._encode_open_round(state["open_round"])
        betting_order_encoding = self._encode_betting_order(state["open_round"]["order"])
        gamemode_encoding = self._encode_gamemode(state["gamemode"])

        return np.concatenate(
            [hand_encoding, open_round_encoding, gamemode_encoding, betting_order_encoding]
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
        Encodes only the played card into a fixed-size representation. 32 bits
        """
        encoding = np.zeros(32)

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
        self.model.model.save_weights("RLeasyAI.weights.h5")

    
    
if __name__ == "__main__":
    env = SkatGameEnvironment()
    state_size = 76
    action_size = 32
    agent = AIAgent(state_size, action_size)

    save_interval = 200
    

    for episode in range(200000):
        state = env.reset()
        done = False

        while not done:

            action_index = agent.act(state)

            next_state, reward, done, win = env.step(action_index)
            
            agent.train(state, action_index, reward, next_state, done)

            agent.remember(state, action_index, reward, next_state, done)

            state = next_state

        agent.replay(agent.batch_size)

        #save the modell all 200 Games
        if (episode + 1) % save_interval == 0:
            print(f"Saving model at episode {episode + 1}")
            agent.save_model()


        print(f"Episode {episode + 1}, Epsilon: {agent.epsilon}")
