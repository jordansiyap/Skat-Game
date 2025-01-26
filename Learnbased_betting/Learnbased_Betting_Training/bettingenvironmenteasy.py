import random

from Logic.deal import Deal
from Rulebased_Betting.betmedium import BetMedium
from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.calculategamemodevalue import CalculateGamemodeValue
from Rulebased_Betting.helpersbetting import HelpersBetting
from Learnbased_betting.Learnbased_Betting_Training.makeaigamemodebet import MakeAIGamemodeBet
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

        self.skataufnahme = True

        self.chosen_gamemode = {"name": "Karo", "betting": "18"}

    def reset(self):
        random.shuffle(self.players)
        self.deal = Deal.deal(self.players)

        self.previous_bets = []

        self.skataufnahme = True

        self.chosen_gamemode = {"name": "Karo", "betting": "18"}

        return self.state()

    def state(self):
        state = {
            "hand": self.deal["hands"][
                list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]],
            "previous_bets": self.previous_bets,
            "skataufnahme": self.skataufnahme,
            "chosen_gamemode": self.chosen_gamemode,
            "skat": self.deal["hands"]["player3"]
        }
        return state


    def step_betting(self, action_index):
        ai_player = {"playerId":
                list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]}
        done = False
        reward = 0

        active_player = NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["next_player"]
        if NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["skatAufnahme"]:
            if active_player == ai_player:
                reward = 0
            else:
                reward = 0
            done = True
            return self.state(),reward,done
        while active_player != ai_player:
            bet = MakeAIGamemodeBet.make_ai_gamemode_bet(self.ai_models[active_player["playerId"]],self.deal["hands"][active_player["playerId"]],self.previous_bets,self.deal["betting_order"])
            self.previous_bets.append({"player": active_player, "gamemode" : bet["gamemode"]})
            active_player = NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["next_player"]
            if NextPlayerBetting.next_player(self.deal["betting_order"], self.previous_bets)["skatAufnahme"]:
                reward = 0
                done = True
                return self.state(),reward,done

        bet_options = [
            "Raise",
            "Pass"
        ]

        action = bet_options[action_index]

        skat_bet_table = HelpersBetting.create_skat_bid_table(active_player)
        next_betting = 0

        if len(self.previous_bets) == 0:
            self.previous_bets.append({"player" : active_player, "gamemode" : {"name" : "Raise", "active_player" : active_player , "betting" : "18"}})
        else:
            if action == "Raise":
                if self.previous_bets[-1].get("gamemode").get("name") == "Pass" or self.previous_bets[-1].get("gamemode").get("name") == "Check":
                    for x in skat_bet_table:
                        if int(x.get("betting")) > int(self.previous_bets[-1].get("gamemode").get("betting")):
                            next_betting = x.get("betting")
                            break
                    if int(next_betting) > 144:
                        reward = -1
                        done = True
                        return self.state(), reward, done
                    self.previous_bets.append({"player": active_player,
                                               "gamemode": {"name": "Raise", "active_player": active_player,
                                                            "betting": next_betting}})
                else:
                    self.previous_bets.append({"player": active_player,
                                               "gamemode": {"name": "Check", "active_player": active_player,
                                                            "betting": self.previous_bets[-1].get("gamemode").get(
                                                                "betting")}})

            else:
                self.previous_bets.append({"player": active_player,
                                           "gamemode": {"name": action, "active_player": active_player,
                                                        "betting": self.previous_bets[-1].get("gamemode").get("betting")}})

        active_player = NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["next_player"]

        if NextPlayerBetting.next_player(self.deal["betting_order"],self.previous_bets)["skatAufnahme"]:
            if active_player == ai_player:
                reward = 0
            else:
                reward = 0
            done = True
            return self.state(),reward,done

        while active_player != ai_player:

            bet = MakeAIGamemodeBet.make_ai_gamemode_bet(self.ai_models[active_player["playerId"]],
                                                         self.deal["hands"][active_player["playerId"]], self.previous_bets,
                                                         self.deal["betting_order"])
            self.previous_bets.append({"player": active_player, "gamemode": bet["gamemode"]})
            active_player = NextPlayerBetting.next_player(self.deal["betting_order"], self.previous_bets)["next_player"]
            if NextPlayerBetting.next_player(self.deal["betting_order"], self.previous_bets)["skatAufnahme"]:
                if active_player == ai_player:
                    reward = 0
                else:
                    reward = 0
                done = True
                return self.state(), reward, done
        return self.state(),reward,done

    def step_take_skat(self,action_index):
        success = False
        player = {"playerId":
                list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]}
        gamemodes = []
        gamemodes_hand =[]
        hand = self.deal["hands"][
                list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]]

        if len(self.previous_bets) != 0:
            last_bet = self.previous_bets[-1].get("gamemode")
        else:
            last_bet = {"name": "Raise", "active_player": player, "betting": "18"}

        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]

        for i in modes:
            if i == "Null":
                gamemodes.append({"name": i, "active_player": player, "description": "Nullspiel", "betting": "23"})
            else:
                multiplier = CalculateGamemodeValue.calculate_multiplier(hand)
                gamemodes.append(CalculateBids.create_gamemode(i, player, multiplier,
                                                            CalculateBids.check_clubs_jack(hand)))
        for i in modes:
            if i == "Null":
                gamemodes_hand.append({"name": i, "active_player": player, "description": "Nullspiel Hand", "betting": "35"})
            else:
                multiplier = CalculateGamemodeValue.calculate_multiplier(hand)
                gamemodes_hand.append(CalculateBids.create_gamemode_hand(i, player, multiplier,
                                                               CalculateBids.check_clubs_jack(hand)))

        gamemodes.sort(key=lambda bet: int(bet.get('betting')))
        gamemodes_hand.sort(key=lambda bet: int(bet.get('betting')))
        actions = [
            "Skat",
            "Hand"
        ]

        action = actions[action_index]

        if action == "Skat":
            self.skataufnahme = True
            if int(gamemodes[-1].get("betting")) < int(last_bet.get("betting")):
                reward = -1
                return self.state(),reward, success
            else:
                reward = 0.1
                success = True
                return self.state(),reward,success
        else:
            self.skataufnahme = False
            if int(gamemodes_hand[-1].get("betting")) < int(last_bet.get("betting")):
                reward = -1
                return self.state(),reward, success
            else:
                reward = 0.1
                success = True
                return self.state(),reward,success


    def step_decide(self,action_index):
        player = {"playerId":
                      list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]}

        hand = self.deal["hands"][
            list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]]

        gamemodes =[]

        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]

        if self.skataufnahme:
            for i in modes:
                if i == "Null":
                    gamemodes.append({"name": i, "active_player": player, "description": "Nullspiel", "betting": "23"})
                else:
                    multiplier = CalculateGamemodeValue.calculate_multiplier(hand)
                    gamemodes.append(CalculateBids.create_gamemode(i, player, multiplier,
                                                                   CalculateBids.check_clubs_jack(hand)))
        else:
            for i in modes:
                if i == "Null":
                    gamemodes.append(
                        {"name": i, "active_player": player, "description": "Nullspiel Hand", "betting": "35"})
                else:
                    multiplier = CalculateGamemodeValue.calculate_multiplier(hand)
                    gamemodes.append(CalculateBids.create_gamemode_hand(i, player, multiplier,
                                                                             CalculateBids.check_clubs_jack(hand)))

        action = gamemodes[action_index]

        if len(self.previous_bets) != 0:
            last_bet = self.previous_bets[-1].get("gamemode")
        else:
            last_bet = {"name": "Raise", "active_player": player, "betting": "18"}

        self.chosen_gamemode = action


        if action.get("betting") < last_bet.get("betting"):
            reward = -1
            success = False
            return self.state(),reward,success
        else:
            if self.skataufnahme:
                reward = self.reward_function(hand)
            else:
                reward = 0.1
            success = True
            return self.state(),reward,success

    def step_discard(self,action_index):
        player = {"playerId":
                      list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]}

        hand = self.deal["hands"][
            list(self.ai_models.keys())[list(self.ai_models.values()).index("RL Bot (Weakest)")]]

        skat = self.deal["hands"]["player3"]

        skat_hand = []

        for i in hand[:]:
            skat_hand.append(i)

        for i in skat[:]:
            skat_hand.append(i)


        skat_hand.sort(key = lambda x: (x.get("suit"),x.get("value")))

        options = []

        reduced_skat_hand = skat_hand[:]

        for i in skat_hand:
            cards = []
            cards.append(i)
            reduced_skat_hand.remove(i)
            for j in reduced_skat_hand:
                cards.append(j)
                options.append(cards[:])
                cards.remove(j)

        action = options[action_index]

        new_hand = skat_hand[:]

        for i in action:
            new_hand.remove(i)

        gamemode = self.chosen_gamemode.get("name")

        if gamemode != "Null":
            if self.skataufnahme:
                obj = CalculateBids.create_gamemode(gamemode, player, CalculateGamemodeValue.calculate_multiplier(new_hand),
                                                    CalculateBids.check_clubs_jack(new_hand))
            else:
                obj = CalculateBids.create_gamemode_hand(gamemode, player,
                                                    CalculateGamemodeValue.calculate_multiplier(new_hand),
                                                    CalculateBids.check_clubs_jack(new_hand))
        else:
            if self.skataufnahme:
                obj = {"name": "Null", "active_player": player, "description": "Nullspiel", "betting": "23"}
            else:
                obj = {"name": "Null", "active_player": player, "description": "Nullspiel", "betting": "35"}


        if len(self.previous_bets) != 0:
            if int(obj.get("betting")) < int(self.previous_bets[-1].get("gamemode").get("betting")):
                reward = -1
                success = False
                return self.state_discard(new_hand,action),reward,success
            else:
                reward = 0.2 + self.reward_function(new_hand)
                success = True
                return self.state_discard(new_hand, action), reward, success
        else:
            if int(obj.get("betting")) < 18:
                reward = -1
                success = False
                return self.state_discard(new_hand,action),reward,success
            else:
                reward = 0.2 + self.reward_function(new_hand)
                success = True
                return self.state_discard(new_hand, action), reward, success

    def reward_function(self,hand):
        count = BetMedium.count_jacks(hand)
        if count >=2:
            return count*0.25
        else:
            return (2-count)*-0.1

    def state_discard(self,hand, skat):
        state = {
            "hand": hand,
            "previous_bets": self.previous_bets,
            "skataufnahme": self.skataufnahme,
            "chosen_gamemode": self.chosen_gamemode,
            "skat": skat
        }
        return state
















