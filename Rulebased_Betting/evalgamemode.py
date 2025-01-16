from flask import request

from deceasy import DecEasy

class EvalGamemode:
    @staticmethod
    def eval_gamemode():
        data = request.json
        previous_bets = data.get("previous_bets")
        player_hands = data.get("player_hands")
        ai_model = data.get("ai_model")

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



        hand = player_hands[winning_player]
        skat = player_hands["player3"]


        return {"selected_gamemode":{"gamemode":DecEasy.make_decision_easy(hand,skat,winning_bid,winning_player),
                                             "player": winning_player},"player_order_next_round": player_order_next_round}





