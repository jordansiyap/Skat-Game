from flask import request

from deceasy import DecEasy

class EvalGamemode:
    @staticmethod
    def eval_gamemode(data):
        previous_bets = data.get("previous_bets")
        player_hands = data.get("player_hands")
        ai_model = data.get("ai_model")

        player_order_next_round = []

        if previous_bets[0].get("player") == "Player2":
            player_order_next_round.append("Player1")
            player_order_next_round.append("Player2")
            player_order_next_round.append("Player0")
        elif previous_bets[0].get("player") == "Player1":
            player_order_next_round.append("Player0")
            player_order_next_round.append("Player1")
            player_order_next_round.append("Player2")
        elif previous_bets[0].get("player") == "Player0":
            player_order_next_round.append("Player2")
            player_order_next_round.append("Player0")
            player_order_next_round.append("Player1")
        else:
            return {"error message": "impossible player order"}

        winning_bid = previous_bets[-2].get("gamemode")
        winning_player = previous_bets[-2].get("player")

        if winning_player == "Player0":
            hand = player_hands["player0"]
        elif winning_player == "Player1":
            hand = player_hands["player1"]
        elif winning_player == "Player2":
            hand = player_hands["player2"]        

        skat = player_hands["skat"]

        return {"selected_gamemode":{"gamemode":DecEasy.make_decision_easy(hand,skat,winning_bid,winning_player),
                                             "player": winning_player},"player_order_next_round": player_order_next_round}




