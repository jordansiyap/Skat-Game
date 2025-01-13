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

        if previous_bets[0].get("player") == "player4":
            player_order_next_round.append("player2")
            player_order_next_round.append("player4")
            player_order_next_round.append("player1")
        elif previous_bets[0].get("player") == "player2":
            player_order_next_round.append("player1")
            player_order_next_round.append("player2")
            player_order_next_round.append("player4")
        elif previous_bets[0].get("player") == "player1":
            player_order_next_round.append("player4")
            player_order_next_round.append("player1")
            player_order_next_round.append("player2")
        else:
            return {"error message": "impossible player order"}

        winning_bid = previous_bets[-2].get("gamemode")
        winning_player = previous_bets[-2].get("player")


        for i in range(len(player_hands)):
            x = player_hands[i]
            if winning_player in x:
                hand = x.get(winning_player)
            elif "player3" in x:
                skat = x.get('player3')

        return {"selected_gamemode":{"gamemode":DecEasy.make_decision_easy(hand,skat,winning_bid,winning_player),
                                             "player": winning_player},"player_order_next_round": player_order_next_round}





