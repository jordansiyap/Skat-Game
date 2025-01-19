from flask import request

from Rulebased_Betting.deceasy import DecEasy
from Rulebased_Betting.dechard import DecHard
from Rulebased_Betting.decmedium import DecMedium


class EvalGamemode:
    @staticmethod
    def eval_gamemode():
        data = request.json
        previous_bets = data.get("previous_bets")
        player_hands = data.get("player_hands")
        ai_model = data.get("ai_model")
        player = data.get("player")

        player_order_next_round = []

        player_order_next_round.append(previous_bets[1].get("player"))
        player_order_next_round.append(previous_bets[0].get("player"))
        for idx, elem in enumerate(previous_bets):
            thiselem = elem
            nextelem = previous_bets[(idx+1)%len(previous_bets)]
            if thiselem.get("gamemode").get("name") == "Pass":
                player_order_next_round.append(nextelem.get("player"))
                break

        counter_passes = 0
        for idx, elem in enumerate(previous_bets):
            thiselem = elem
            nextelem = previous_bets[(idx-1)%len(previous_bets)]
            if thiselem.get("gamemode").get("name") == "Pass":
                counter_passes +=1
                if counter_passes == 2:
                    winning_bid = nextelem.get("gamemode")
                    winning_player=nextelem.get("player")
                    break

        if player != winning_player:
            return {"error" : "player hasnt won the betting"}

        '''hand = player_hands[winning_player]
        skat = player_hands["player3"]'''

        ai_choice = {"gamemode": "initialise", "player_hands": "initialise"}

        if ai_model == "Easy Rule-based Bot":
            ai_choice = DecEasy.make_decision_easy(player_hands, winning_bid, winning_player)
        elif ai_model == "Average Rule-based Bot":
            ai_choice = DecMedium.make_decision_medium(player_hands, winning_bid, winning_player)
        elif ai_model == "Hardest Rule-based Bot":
            ai_choice = DecHard.make_decision_hard(player_hands, winning_bid, player)

        return {"selected_gamemode": {"gamemode": ai_choice.get("gamemode"),
                                      "player": winning_player}, "player_order_next_round": player_order_next_round,
                "player_hands": ai_choice.get("player_hands")}







