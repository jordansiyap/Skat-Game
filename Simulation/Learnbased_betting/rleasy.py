import keras
import numpy as np

from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.calculategamemodevalue import CalculateGamemodeValue
from Rulebased_Betting.helpersbetting import HelpersBetting
from pathlib import Path

"""Leichter Lernbasierter Agent
Lädt ein gespeichertes Modell
Entscheidungs-Methoden für das Reizen und Auswählen
Kodiert den Zustand in einen Vektor"""


class RLEasy:
    def __init__(self):
        path = Path.cwd()
        self.model_betting = keras.saving.load_model(Path(str(path)+"/Learnbased_betting/model_betting_easy.keras"))
        self.model_skataufnahme = keras.saving.load_model(Path(str(path)+"/Learnbased_betting/model_skataufnahme_easy.keras"))
        self.model_decide = keras.saving.load_model(Path(str(path)+"/Learnbased_betting/model_decide_easy.keras"))
        self.model_discard = keras.saving.load_model(Path(str(path)+"/Learnbased_betting/model_discard_easy.keras"))


    def act_bet(self,hand,previous_bets,player):
        state = self.state_bet(hand,previous_bets)
        state_vector = self.encode_state_bet(state)
        action_index = np.argmax(self.model_betting.predict(state_vector)[0])

        bet_options = [
            "Raise",
            "Pass"
        ]

        action = bet_options[action_index]
        if action == "Raise":
            skat_bet_table = HelpersBetting.create_skat_bid_table(player)
            if previous_bets[-1].get("gamemode").get("name") == "Pass" or previous_bets[-1].get(
                    "gamemode").get("name") == "Check":
                next_betting = int(previous_bets[-1].get("gamemode").get("betting"))
                for x in skat_bet_table:
                    if int(x.get("betting")) > next_betting:
                        next_betting = x.get("betting")
                        break
                return {"player": player,"gamemode": {"name": "Raise", "active_player": player,
                                                        "betting": str(next_betting)}}
            else:
                return {"player": player,
                                           "gamemode": {"name": "Check", "active_player": player,
                                                        "betting": previous_bets[-1].get("gamemode").get(
                                                            "betting")}}
        else:
            return {"player": player,
                                       "gamemode": {"name": action, "active_player": player,
                                                    "betting": previous_bets[-1].get("gamemode").get("betting")}}

    def act_decide(self,hand,previous_bets,player,skat):
        state = self.state_bet(hand,previous_bets)
        state_vector = self.encode_state_skataufnahme(state)

        action_index = np.argmax(self.model_skataufnahme.predict(state_vector)[0])

        if action_index == 0:
            skataufnahme = True
        else:
            skataufnahme = False

        next_state = self.state_decide(hand,previous_bets, skataufnahme)
        next_vector = self.encode_state_decide(next_state)

        action_index = np.argmax(self.model_decide.predict(next_vector)[0])

        gamemodes = []

        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]

        if skataufnahme:
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

        gamemode = gamemodes[action_index]

        if skataufnahme:
            final_state = self.state_discard(hand,previous_bets, skataufnahme, gamemode, skat)
            final_state_vector = self.encode_state_discard(final_state)

            action_index = np.argmax(self.model_discard.predict(final_state_vector))

            skat_hand = []

            for i in hand[:]:
                skat_hand.append(i)

            for i in skat[:]:
                skat_hand.append(i)

            skat_hand.sort(key=lambda x: (x.get("suit"), x.get("value")))

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

            return gamemode,new_hand,action
        else:
            return gamemode,hand,skat



    def state_bet(self,hand,previous_bets):
        state = {
            "hand": hand,
            "previous_bets": previous_bets
        }
        return state

    def state_decide(self,hand,previous_bets,skataufnahme):
        state = {
            "hand": hand,
            "previous_bets": previous_bets,
            "skataufnahme": skataufnahme
        }
        return state

    def state_discard(self,hand,previous_bets,skataufnahme,gamemode,skat):
        state = {
            "hand": hand,
            "previous_bets": previous_bets,
            "skataufnahme": skataufnahme,
            "chosen_gamemode": gamemode,
            "skat": skat
        }
        return state

    def encode_state_bet(self, state):
        hand_vector = self.encode_hand(state.get("hand"))
        gamemode_vector = np.zeros(11)

        next_betting = 18
        if len(state.get("previous_bets")) != 0:
            if state.get("previous_bets")[-1].get("gamemode").get("name") == "Raise":
                next_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))
            else:
                skat_bet_table = HelpersBetting.create_skat_bid_table(state.get("previous_bets")[-1].get("player"))
                for x in skat_bet_table:
                    if int(x.get("betting")) > int(state.get("previous_bets")[-1].get("gamemode").get("betting")):
                        next_betting = int(x.get("betting"))
                        break

        next_betting_vector = np.array(list(np.binary_repr(next_betting).zfill(8))).astype(np.int8)
        bet_options = [
            "Raise",
            "Check",
            "Pass"
        ]
        players = [
            "player1",
            "player2",
            "player4"
        ]
        index = 0
        for bet in state["previous_bets"]:
            if bet["gamemode"].get("name") == "Pass":
                gamemode_vector[index] = 1
                index += 1
                if index == 2:
                    break
        bets = reversed(state["previous_bets"])
        for i, bet in enumerate(bets):
            index_bet = 2 + i * 3 + bet_options.index(bet["gamemode"].get("name"))
            gamemode_vector[index_bet] = 1
            if i == 0:
                gamemode_vector[8 + players.index(bet["player"])] = 1
            if i == 1:
                break

        state_vector = np.concatenate((hand_vector, gamemode_vector, next_betting_vector)).reshape(1, -1)
        return state_vector

    def encode_state_skataufnahme(self,state):
        player = "player1"
        hand_vector = self.encode_hand(state.get("hand"))

        betting_vector = np.zeros(0)

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
                betting = 23
            else:
                multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                betting = int(CalculateBids.create_gamemode(i,player,multiplier,CalculateBids.check_clubs_jack(state.get("hand"))).get("betting"))
            vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
            betting_vector = np.concatenate((betting_vector,vector))
        for i in modes:
            if i == "Null":
                betting = 35
            else:
                multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                betting = int(CalculateBids.create_gamemode_hand(i,player,multiplier,CalculateBids.check_clubs_jack(state.get("hand"))).get("betting"))
            vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
            betting_vector = np.concatenate((betting_vector,vector))

        winner_betting = 18
        if len(state.get("previous_bets")) !=0:
            winner_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))

        winning_vector = np.array(list(np.binary_repr(winner_betting).zfill(8))).astype(np.int8)

        state_vector = np.concatenate((hand_vector,winning_vector,betting_vector))
        return state_vector.reshape(1,-1)

    def encode_state_decide(self, state):
        player = "player1"
        hand_vector = self.encode_hand(state.get("hand"))

        skat_vector = np.zeros(1)

        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]

        betting_vector = np.zeros(0)

        if state.get("skataufnahme"):
            skat_vector[0] = 1
            for i in modes:
                if i == "Null":
                    betting = 23
                else:
                    multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                    betting = int(CalculateBids.create_gamemode(i, player, multiplier,
                                                                CalculateBids.check_clubs_jack(state.get("hand"))).get(
                        "betting"))
                vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
                betting_vector = np.concatenate((betting_vector, vector))
        else:
            for i in modes:
                if i == "Null":
                    betting = 35
                else:
                    multiplier = CalculateGamemodeValue.calculate_multiplier(state.get("hand"))
                    betting = int(CalculateBids.create_gamemode_hand(i, player, multiplier,
                                                                     CalculateBids.check_clubs_jack(
                                                                         state.get("hand"))).get("betting"))
                vector = np.array(list(np.binary_repr(betting).zfill(8))).astype(np.int8)
                betting_vector = np.concatenate((betting_vector, vector))

        winner_betting = 18
        if len(state.get("previous_bets")) != 0:
            winner_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))

        winning_vector = np.array(list(np.binary_repr(winner_betting).zfill(8))).astype(np.int8)

        state_vector = np.concatenate((hand_vector, skat_vector, winning_vector, betting_vector)).reshape(1, -1)
        return state_vector

    def encode_state_discard(self,state):
        hand = state.get("hand")
        skat = state.get("skat")

        for i in skat:
            hand.append(i)
        hand_vector = self.encode_hand(hand)

        gamemode_vector = np.zeros(6)
        modes = [
            "Kreuz",
            "Pik",
            "Herz",
            "Karo",
            "Grand",
            "Null"
        ]
        gamemode = state.get("chosen_gamemode").get("name")
        for i in modes:
            if i == modes:
                gamemode[modes.index(i)] = 1

        winner_betting = 18
        if len(state.get("previous_bets")) != 0:
            winner_betting = int(state.get("previous_bets")[-1].get("gamemode").get("betting"))

        winning_vector = np.array(list(np.binary_repr(winner_betting).zfill(8))).astype(np.int8)

        state_vector =  np.concatenate((hand_vector,gamemode_vector,winning_vector)).reshape(1,-1)
        return state_vector

    def encode_hand(self, hand):
        suits = ["clubs", "spades", "hearts", "diamonds"]
        values = ["ace", "king", "queen", "jack", "10", "9", "8", "7"]
        encoding = np.zeros((len(suits), len(values)))

        for card in hand:
            suit_index = suits.index(card["suit"])
            value_index = values.index(card["value"])
            encoding[suit_index][value_index] = 1

        return encoding.flatten()
