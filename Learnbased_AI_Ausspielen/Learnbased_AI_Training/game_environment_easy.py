import random
import eval_round
import deal
import eval_gamee
from easy_RB_AI import easy_AI


class SkatGameEnvironment:
    def __init__(self):
        self.dealer = deal.Deal()
        self.gamemode_name = ["Grand", "Nullspiel", "Kreuz", "Pik", "Herz", "Karo"]
        self.players = ["player1", "player2", "player4"]
        self.ai_player = "player1"  # The learning AI is player1
        self.other_ai_player = {"player2": easy_AI(), "player4": easy_AI()}
        self.count_step = 0
        self.reset()

    def reset(self):
        
        deal_result = self.dealer.deal(self.players)
        self.hands = deal_result["hands"]
        self.betting_order = deal_result["betting_order"]
        self.skat = deal_result["skat"]
        self.current_round = 0
        self.history = {"rounds": [], "betting_order": self.betting_order}
        self.open_round = {
            "order": self.betting_order,
            "cards": {}
        }

        self.gamemode = {
            "name": random.choice(self.gamemode_name),
            "active_player": self.betting_order[0],
        }
        return self._get_state()

    def _get_state(self):
        """
        Constructs the state representation for the AI.
        """
        # Get the hand of the easy-learning-based AI
        hand = None
        for h in self.hands:
            if self.ai_player in h:
                hand = h[self.ai_player]
                break

        state = {
            "hand": hand[:],
            "open_round": dict(self.open_round),
            "gamemode": dict(self.gamemode),
            "turn_order": self.betting_order[:]
        }

        return state
    
    
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


    def _get_card_value(self, card):
        """Helper für Kartenpunktbewertung"""
        point_table = {
            "ace": 11, "10": 10, "king": 4, 
            "queen": 3, "jack": 2, "9": 0, 
            "8": 0, "7": 0
        }
        return point_table.get(card["value"], 0)
    
    

    def step(self, action_index):
        # Play the selected card
        #print("HISTORY LENGTH : ", len(self.history["rounds"]))
        win = False
        hand = None
        done = False
        reward = 0
        for h in self.hands:
            if self.ai_player in h:
                hand = h[self.ai_player]
                break


        action = self.get_card_from_index(action_index) 
        print(action_index, " : ", action)          
        hand.remove(action)


        # AI plays the card
        self.open_round["cards"][self.ai_player] = action

        # Rule-based AIs play their cards
        for player in self.betting_order:
            if player != self.ai_player:
                if player not in self.open_round["cards"] :
                    #find the hand of this Rule-based
                    rule_based_ai_hand = None
                    for h in self.hands:
                        if player in h:
                            rule_based_ai_hand = h[player]
                            break
                    #process move
                    #print("Open_roundd : ", self.open_round)
                    move = self.other_ai_player[player].ai_move(self.open_round, self.gamemode, rule_based_ai_hand, self.history)
                    self.open_round["cards"][player] = move["play_card"]
                    #rule_based_ai_hand.remove(move["play_card"])

        # Evaluate the round
        round_evaluator = eval_round.eval_round()
        round_result = round_evaluator.eval_round(self.open_round["cards"], self.gamemode.get("name"), self.open_round["order"])
        self.history["rounds"].append(round_result)

        # Initialize reward components
        round_winner_reward = 0
        strategic_reward = 0

        if round_result["winner"] == self.ai_player:
            round_winner_reward = 15
        else:
            round_winner_reward = -10

        gamemode = self.gamemode["name"]

        if gamemode == "Nullspiel":

            if round_result["winner"] != self.ai_player:
                strategic_reward += 25
            
            elif round_result["winner"] == self.ai_player:
                strategic_reward -= 25

        # Check if the game is over
        done = len(self.history["rounds"]) >= 10

        reward = round_winner_reward + strategic_reward
    

        #prepare the next round
        if not done :
            # Gewinner dieser Runde wird Vorhand für die nächste Runde
            winner = round_result["winner"]
            winner_index = self.betting_order.index(winner)
            new_order = self.betting_order[winner_index:] + self.betting_order[:winner_index]
            self.betting_order = new_order

            # new open_rounf for the next round
            self.open_round = {"order": self.betting_order, "cards": {}}

            #Die andere rule-based AIs spielen schon ihre Karte des nächsten Zug bis die learning-based AI dran ist
            for player in self.betting_order:
                #print(player," -- ", self.ai_player)
                if player == self.ai_player:
                    #print(player," -- ", self.ai_player, " The Player is the AI: On break")
                    break
                else:
                    if player not in self.open_round["cards"] :
                        rule_based_ai_hand = None
                        for h in self.hands:
                            if player in h:
                                rule_based_ai_hand = h[player]
                                break
                        #process move
                        move = self.other_ai_player[player].ai_move(self.open_round, self.gamemode, rule_based_ai_hand, self.history)
                        self.open_round["cards"][player] = move["play_card"]
                        #rule_based_ai_hand.remove(move["play_card"])

        return self._get_state(), reward, done, win