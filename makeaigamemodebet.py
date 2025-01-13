from flask import request

from betmedium import BetMedium
from beteasy import BetEasy

class MakeAIGamemodeBet:
    @staticmethod
    def make_ai_gamemode_bet():
        make_ai_gamemode_bet = request.json
        ai_model = make_ai_gamemode_bet.get("ai_model")
        hand = make_ai_gamemode_bet.get("hand")
        previous_bets = make_ai_gamemode_bet.get("previous_bets")
        player = previous_bets[-1].get("active_player")

        if ai_model == "easy":
            return MakeAIGamemodeBet.get_next_bid(BetEasy.betting_ai_easy(hand, previous_bets, player), player)
        elif ai_model =="medium":
            return MakeAIGamemodeBet.get_next_bid(BetMedium.betting_ai_medium(hand, previous_bets, player), player)

    @staticmethod
    def create_skat_bid_table(player):
        skat_bid_table = [
            {"name": "Null", "active_player": player, "description": "Nullspiel", "betting": "23"},
            {"name": "Null", "active_player": player, "description": "Nullspiel Hand", "betting": "35"},
        ]

        modes = ["Karo", "Herz", "Pik", "Kreuz", "Grand"]

        for mode in modes:
            for x in range(1,6):
                bid = MakeAIGamemodeBet.create_gamemode(mode, player, x)
                y = next((y for y in skat_bid_table if int(y["betting"])==int(bid["betting"])),None)
                if y is None:
                    skat_bid_table.append(bid)
        skat_bid_table.sort(key = lambda bet: int(bet['betting']))
        return skat_bid_table

    @staticmethod
    def create_gamemode(mode, player, number):
        if mode == "Karo":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 9)}
        elif mode == "Herz":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 10)}
        elif mode == "Pik":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 11)}
        elif mode == "Kreuz":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 12)}
        elif mode == "Grand":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 24)}

    @staticmethod
    def get_next_bid(result,player):
        skat_bid_table = MakeAIGamemodeBet.create_skat_bid_table(player)
        if int(result[-1]["betting"]) == int(result[-2]["betting"]):
            y = next((y for y in skat_bid_table if int(y["betting"]) == int(result[-1]["betting"])), None)
            return y
        else:
            y = next((y for y in skat_bid_table if int(y["betting"]) > int(result[-2]["betting"])), None)
            return y