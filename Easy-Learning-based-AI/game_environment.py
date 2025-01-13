import random
import eval_round
import deal
import eval_gamee
from easy_RB_AI import easy_AI


class SkatGameEnvironment:
    def __init__(self):
        self.dealer = deal.Deal()
        self.gamemode_name = ["Grand", "Nullspiel", "Kreuz", "Pik", "Herz", "Karo"]
        self.players = ["player1", "player2", "player3"]
        self.ai_player = "player1"  # The learning AI is player1
        self.rule_based_ai = {"player2": easy_AI(), "player3": easy_AI()}
        self.count_step = 0
        self.reset()

    def reset(self):
        # Deal new cards
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

        # Construct the state
        state = {
            "hand": hand[:],
            "open_round": dict(self.open_round),
            "gamemode": dict(self.gamemode),
            "turn_order": self.betting_order[:]
        }

        return state
    

    def step(self, action_index):
        # Play the selected card
        #print("HISTORY LENGTH : ", len(self.history["rounds"]))
        print("We Enter Step")
        hand = None
        done = False
        reward = 0
        for h in self.hands:
            if self.ai_player in h:
                hand = h[self.ai_player]
                break

        # a card that doesm't exist has been predicted
        if action_index >= len(hand):
            reward = -40
            done = False
            print("REWARD : ", reward)
            return self._get_state(), reward, done  # Illegal move
        
        
        action = hand.pop(action_index)
        
        card_to_try = {
                "open_round": self.open_round,
                "gamemode": self.gamemode,
                "check_card": action,
                "hand": hand
        }

        if not self.open_round.get("cards"):
            is_legal = {"status": "true"}
        else:    
            is_legal = self.rule_based_ai["player2"].get_is_legal_move(card_to_try)

        if is_legal.get("status") == "false":
            reward = -20
            done = False
            hand.appen(action)
            print("REWARD : ", reward)
            return self._get_state(), reward, done  # Illegal move
        # else es is legal, jetzt schauen wir ob die nicht angespielt hat. Falls ja reward 20, falls nein reward bleibt 0.
        elif self.open_round.get("cards") and is_legal.get("wahlfrei") == "false":
            reward = 40
            print("REWARD : ", reward)
        else: #reward bleib 0 (anspielen oder wahlfrei bei bedienen)
            reward = 0
            print("REWARD : ", reward)

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
                    move = self.rule_based_ai[player].ai_move(self.open_round, self.gamemode, rule_based_ai_hand, self.history)
                    self.open_round["cards"][player] = move["play_card"]
                    #rule_based_ai_hand.remove(move["play_card"])

        # Evaluate the round
        round_evaluator = eval_round.eval_round()
        round_result = round_evaluator.eval_round(self.open_round["cards"], self.gamemode.get("name"), self.open_round["order"])
        self.history["rounds"].append(round_result)

        # Check if the game is over
        done = len(self.history["rounds"]) >= 10
        

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
                        #find the hand of this Rule-based
                        rule_based_ai_hand = None
                        for h in self.hands:
                            if player in h:
                                rule_based_ai_hand = h[player]
                                break
                        #process move
                        move = self.rule_based_ai[player].ai_move(self.open_round, self.gamemode, rule_based_ai_hand, self.history)
                        self.open_round["cards"][player] = move["play_card"]
                        #rule_based_ai_hand.remove(move["play_card"])

        #reward the learning-based- AI, if the round has been won.
        #if round_result["winner"] == self.ai_player :
            #reward = reward + 3
        #else :
            #reward = reward - 3

        #if done :
            #game_result = eval_gamee.eval_game(self.history, self.gamemode)
        print("We quit step")    
        return self._get_state(), reward, done 