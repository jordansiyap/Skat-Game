from flask import request

from deceasy import DecEasy

class MakeAIGaemodeDecision:
    @staticmethod
    def get_gamemode_decision():
        get_gamemode_decision =  request.json
        ai_model = get_gamemode_decision.get("ai_model")
        hand = get_gamemode_decision.get("hand")
        skat = get_gamemode_decision.get("skat")
        winning_bid = get_gamemode_decision.get("gamemode")
        player = winning_bid.get("active_player")

        if ai_model == "easy":
            return DecEasy.make_decision_easy(hand, skat, winning_bid, player)