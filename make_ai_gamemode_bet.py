import random

from flask import request
from calculate_bids import Calculate_Bids
from bet_medium import Bet_Medium

class Make_AI_Gamemode_Bet():
    def make_ai_gamemode_bet(self):
        make_ai_gamemode_bet = request.json
        ai_model = make_ai_gamemode_bet.get("ai_model")
        hand = make_ai_gamemode_bet.get("hand")
        previous_bets = make_ai_gamemode_bet.get("previous_bets")
        player = previous_bets[-1].get("active_player")

        if ai_model == "easy":
            return betting_ai_easy(hand, previous_bets, player)
        elif ai_model =="medium":
            utily_obj = Bet_Medium()
            return utily_obj.betting_ai_medium(hand,previous_bets,player)

def betting_ai_easy(hand,previous_bets,player):
    utily_obj = Calculate_Bids()
    valid_bets = utily_obj.calculate_bids(hand,player)
    valid_bets.sort(key = lambda bet: int(bet['betting']))
    last_bid = previous_bets[-1]

    ran = random.randint(1,10)
    if ran >=7:
        for x in valid_bets:
            if int(x.get("betting")) > int(last_bid.get("betting")):
                return x
    else:
        return last_bid