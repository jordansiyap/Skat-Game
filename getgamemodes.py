from flask import request

from helpersbetting import HelpersBetting
from makeaigamemodebet import MakeAIGamemodeBet

class GetGamemodes:
    @staticmethod
    def get_gamemodes():
        data = request.json
        player = data.get("player")
        hand = data.get("hand")
        previous_bets = data.get("previous_bets")
        player_order = data.get("players")

        if not previous_bets:
            return {"gamemodes": [{"name": "Raise", "active_player": player, "betting": 18},
                                  ]}
        else:
            if previous_bets[-1].get("gamemode").get("name") == "Pass":
                return {"gamemodes": [{"name": "Raise", "active_player": player, "betting": GetGamemodes.get_next_bid_raise(previous_bets[-1].get("gamemode"),player)},
                                  {"name": "Pass", "active_player": player, "betting": GetGamemodes.get_next_bid(previous_bets[-1].get("gamemode"),player)}]}
            elif previous_bets[-1].get("gamemode").get("name") == "Check":
                return {"gamemodes": [{"name": "Raise", "active_player": player, "betting": GetGamemodes.get_next_bid_raise(previous_bets[-1].get("gamemode"),player)},
                                      {"name": "Pass", "active_player": player, "betting": GetGamemodes.get_next_bid(previous_bets[-1].get("gamemode"),player)}]}
            elif previous_bets[-1].get("gamemode").get("name") == "Raise":
                return {"gamemodes": [{"name": "Check", "active_player": player, "betting": GetGamemodes.get_next_bid(previous_bets[-1].get("gamemode"),player)},
                                      {"name": "Pass", "active_player": player, "betting": GetGamemodes.get_next_bid(previous_bets[-1].get("gamemode"),player)}]}
            else:
                return {"error message": "no valid bet input"}


    #Wiedergabe aller Spielarten
    #Die Methode definiert die von der Skat-KI angebotenen Spielarten Null, Farbspiel und Grand zu Informationszwecken.
    #Die Methode soll keine Informationen über die aktuell gespielte Spielart liefern.
    @staticmethod
    def get_valid_gamemodes():
        valid_gamesmodes = [
            {"name": "Null", "active_player": "player0"},
            {"name": "Kreuz", "active_player": "player0"},
            {"name": "Pik", "active_player": "player0"},
            {"name": "Herz", "active_player": "player0"},
            {"name": "Karo", "active_player": "player0"},
            {"name": "Grand", "active_player": "player0"},
        ]
        return valid_gamesmodes

    @staticmethod
    def get_next_bid(gamemode, player):
        skat_bid_table = HelpersBetting.create_skat_bid_table(player)
        y = next((y for y in skat_bid_table if int(y["betting"]) == int(gamemode["betting"])), None)
        return y["betting"]

    @staticmethod
    def get_next_bid_raise(gamemode, player):
        skat_bid_table = HelpersBetting.create_skat_bid_table(player)
        y = next((y for y in skat_bid_table if int(y["betting"]) > int(gamemode["betting"])), None)
        return y["betting"]
