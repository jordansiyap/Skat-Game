from flask import request

from Learnbased_betting.makerlgamemodebet import MakeRLGamemodeBet
from Rulebased_Betting.deceasy import DecEasy
from Rulebased_Betting.dechard import DecHard
from Rulebased_Betting.decmedium import DecMedium

"""Klasse zur Auswahl des gespielten Spielmodus durch die KI-Agenten
Liest die Schnittstelle aus
Legt die Spielerreihenfolge fest
Übergibt Daten an die KI_Agenten"""
class EvalGamemode:
    @staticmethod
    def eval_gamemode(agent_easy,agent_medium,agent_hard):
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
        last_raise = {}
        for idx, elem in enumerate(previous_bets):
            thiselem = elem
            if thiselem.get("gamemode").get("name") == "Raise":
                last_raise = thiselem
            if thiselem.get("gamemode").get("name") == "Pass":
                counter_passes +=1
                if counter_passes == 2:
                    winning_bid = last_raise.get("gamemode")
                    winning_player=last_raise.get("player")
                    break

        if player != winning_player:
            return {"error" : "player hasnt won the betting"}

        if ai_model == "Easy Rule-based Bot":
            ai_choice = DecEasy.make_decision_easy(player_hands, winning_bid, winning_player)
        elif ai_model == "Average Rule-based Bot":
            ai_choice = DecMedium.make_decision_medium(player_hands, winning_bid, winning_player)
        elif ai_model == "Hardest Rule-based Bot":
            ai_choice = DecHard.make_decision_hard(player_hands, winning_bid, player)
        else:
            ai_choice = MakeRLGamemodeBet.make_decision(ai_model,player_hands,previous_bets,player,agent_easy,agent_medium,agent_hard)

        return {"selected_gamemode": {"gamemode": ai_choice.get("gamemode"),
                                      "player": winning_player}, "player_order_next_round": player_order_next_round,
                "player_hands": ai_choice.get("player_hands")}







