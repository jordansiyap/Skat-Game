import random

import numpy as np
from Logic.deal import Deal
from Rulebased_Betting.helpersbetting import HelpersBetting
from Rulebased_Betting.makeaigamemodebet import MakeAIGamemodeBet
from Rulebased_Betting.nextplayerbetting import NextPlayerBetting


class BettingEnvironmentEasy:
    def __init__(self):
        self.ai_models = {"player1" : "RL Bot (Weakest)",
                        "player2" : "Average Rule-based Bot",
                        "player4" : "Hardest Rule-based Bot"}
        self.players = [{"playerId":"player1"},
                        {"playerId":"player2"},
                        {"playerId":"player4"}
                        ]

        random.shuffle(self.players)
        self.deal = Deal.deal(self.players)

        self.previous_bets = []


    def reset(self):
        random.shuffle(self.players)
        self.deal = Deal.deal(self.players)

        self.previous_bets = []

        return self.state()

    def state(self):
        state = {
            "hand": self.deal["hands"][
                list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]],
            "previous_bets": self.previous_bets
        }
        return state


    def step(self,action_index):
        ai_player = {"playerId":
                list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]}
        done = False
        succesful = False
        reward = 0

        active_player = NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["next_player"]
        if NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["skatAufnahme"]:
            if active_player == ai_player:
                reward = 0.2
            else:
                reward = 0.1
            done = True
            succesful = True
            return self.state(),reward,done, succesful
        while active_player != ai_player:
            bet = MakeAIGamemodeBet.make_ai_gamemode_bet(self.ai_models[active_player["playerId"]],self.deal["hands"][active_player["playerId"]],self.previous_bets,self.deal["betting_order"])
            self.previous_bets.append({"player": active_player, "gamemode" : bet["gamemode"]})
            active_player = NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["next_player"]
            if NextPlayerBetting.next_player(self.deal["betting_order"], self.previous_bets)["skatAufnahme"]:
                reward = 0.1
                done = True
                succesful = True
                return self.state(),reward,done,succesful

        bet_options = [
            "Raise",
            "Check",
            "Pass"
        ]

        action = bet_options[action_index]

        skat_bet_table = HelpersBetting.create_skat_bid_table(active_player)
        next_betting = 0

        if len(self.previous_bets) == 0:
            if action == "Raise":
                self.previous_bets.append({"player" : active_player, "gamemode" : {"name" : action, "active_player" : active_player , "betting" : "18"}})
            else:
                reward = -1
                done = True
                return self.state(),reward,done,succesful
        else:
            if BettingEnvironmentEasy.check_valid_bet(action,self.previous_bets[-1]["gamemode"].get("name")):
                if action == "Raise":
                    for x in skat_bet_table:
                        if int(x["betting"]) > int(self.previous_bets[-1]["gamemode"]["betting"]):
                            next_betting = x["betting"]
                            break
                    self.previous_bets.append({"player": active_player,
                                               "gamemode": {"name": action, "active_player": active_player,
                                                            "betting": next_betting}})

                else:
                    self.previous_bets.append({"player": active_player,
                                               "gamemode": {"name": action, "active_player": active_player,
                                                            "betting": self.previous_bets[-1]["gamemode"]["betting"]}})
            else:
                reward = -1
                done = True
                return self.state(),reward,done,succesful

        active_player = NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["next_player"]

        if NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["skatAufnahme"]:
            if active_player == ai_player:
                reward = 0.2
            else:
                reward = 0.1
            done = True
            succesful = True
            return self.state(),reward,done,succesful

        while active_player != ai_player:

            bet = MakeAIGamemodeBet.make_ai_gamemode_bet(self.ai_models[active_player["playerId"]],
                                                         self.deal["hands"][active_player["playerId"]], self.previous_bets,
                                                         self.deal["betting_order"])
            self.previous_bets.append({"player": active_player, "gamemode": bet["gamemode"]})
            active_player = NextPlayerBetting.next_player(self.deal["betting_order"], self.previous_bets)["next_player"]
            if NextPlayerBetting.next_player(self.deal["betting_order"], self.previous_bets)["skatAufnahme"]:
                if active_player == ai_player:
                    reward = 0.2
                else:
                    reward = 0.1
                done = True
                succesful = True
                return self.state(), reward, done, succesful
        return self.state(),reward,done,succesful

    @staticmethod
    def check_valid_bet(bet,last_bet):
        if bet == "Raise":
            if last_bet == "Raise":
                return False
            else:
                return True
        elif bet == "Check":
            if last_bet == "Raise":
                return True
            else:
                return False
        elif bet == "Pass":
            return True