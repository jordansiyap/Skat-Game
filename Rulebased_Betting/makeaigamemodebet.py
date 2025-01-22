from flask import request

from Rulebased_Betting.bethard import BetHard
from Rulebased_Betting.betmedium import BetMedium
from Rulebased_Betting.beteasy import BetEasy
from Rulebased_Betting.helpersbetting import HelpersBetting
from Rulebased_Betting.nextplayerbetting import NextPlayerBetting


class MakeAIGamemodeBet:
    @staticmethod
    def make_ai_gamemode_bet():
        make_ai_gamemode_bet = request.json
        ai_model = make_ai_gamemode_bet.get("ai_model")
        hand = make_ai_gamemode_bet.get("hand")
        previous_bets = make_ai_gamemode_bet.get("previous_bets")
        player_order = make_ai_gamemode_bet.get("players")

        if not previous_bets:
            return {"gamemde" : {"name": "Raise", "active_player": player_order[0], "betting": 18}}
        else:
            player = NextPlayerBetting.next_player(player_order,previous_bets).get("next_player")

            if ai_model == "Easy Rule-based Bot":
                return MakeAIGamemodeBet.get_next_bid(BetEasy.betting_ai_easy(hand,previous_bets,player),player,previous_bets)
            elif ai_model == "Average Rule-based Bot":
                return MakeAIGamemodeBet.get_next_bid(BetMedium.betting_ai_medium(hand,previous_bets,player),player,previous_bets)
            elif ai_model == "Hardest Rule-based Bot":
                return MakeAIGamemodeBet.get_next_bid(BetHard.betting_ai_hard(hand,previous_bets,player),player,previous_bets)


    @staticmethod
    def get_next_bid(result,player,previous_bets):
        skat_bid_table = HelpersBetting.create_skat_bid_table(player)
        if int(result[-1]["betting"]) == int(result[-2]["betting"]):
            return {"gamemode" : {"name": "Pass", "active_player": player, "betting": previous_bets[-1].get("gamemode").get("betting")}}
        else:
            y = next((y for y in skat_bid_table if int(y["betting"]) > int(result[-2]["betting"])), None)
            if previous_bets[-1].get("gamemode").get("name") == "Check" or previous_bets[-1].get("gamemode").get("name") == "Pass":
                return {"gamemode" : {"name": "Raise", "active_player": player, "betting": y.get("betting")}}
            else:
                return {"gamemode" : {"name": "Check", "active_player": player, "betting": previous_bets[-1].get("gamemode").get("betting")}}
