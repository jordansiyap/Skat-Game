import numpy as np
import os
from .model import Model
from .utils import get_is_legal_move

class RLmedium:
    def __init__(self, model_path=None):

        if model_path is None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            model_path = os.path.join(dir_path, "RLmediumAI.weights.h5")
        self.state_size = 76
        self.action_size = 32
        self.model = Model(self.state_size, self.action_size)
        self.model.model.load_weights(model_path)

    def ai_move(self, open_round, gamemode, hand, history):
        
        state = {
            "hand": hand[:],
            "open_round": dict(open_round),
            "gamemode": dict(gamemode),
            "turn_order": open_round.get("order")[:]
        }

        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]

    
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

        # Exploit: Mask illegal actions in model predictions
        state_vector = self._state_to_vector(state)
        action_probs = self.make_prediction(state)[0]
        masked_probs = np.full_like(action_probs, -np.inf)
        for idx in legal_actions_indexe:
            masked_probs[idx] = action_probs[idx]
        action_index = np.argmax(masked_probs)
    
        print("We Quit act")
        return {"play_card": self.get_card_from_index(action_index)}
    
    def make_prediction(self, state):

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

        state_vector = self._state_to_vector(state)
        action_probs = self.model.predict(state_vector)
        masked_probs = np.full_like(action_probs[0], -np.inf)
        for idx in legal_actions_indexe:
            masked_probs[idx] = action_probs[0][idx]

        action_probs[0] = masked_probs
     
        return action_probs
    
    def get_card_from_index(self, index):
    
        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]
    
        # Calculate suit and value indices
        suit_index = index // len(values)
        value_index = index % len(values)
    
        return {
            "suit": suits[suit_index],
            "value": values[value_index]
        }

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