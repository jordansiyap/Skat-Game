from flask import request

from Rulebased_Betting.helpersbetting import HelpersBetting

"""Klasse zur Rückgabe der für den menschlichen Spieler verfügbaren Spielmodi"""
class GetGamemodes:

    """
    Liest die Schnittstelle aus
    Wählt mögliche Spielmodi basierend auf den bisher gewählten Spielmodi aus
    """
    @staticmethod
    def get_gamemodes():
        data = request.json
        player = data.get("player")
        previous_bets = data.get("previous_bets")

        if not previous_bets:
            return {"gamemodes": [{"name": "Raise", "active_player": player, "betting": 18},
                                  ]}
        else:
            counter = 0
            for x in previous_bets:
                if x.get("gamemode").get("name") == "Pass":
                    counter += 1
            if counter == 2:
                return {"gamemodes": GetGamemodes.get_valid_gamemodes(player)}
            elif previous_bets[-1].get("gamemode").get("name") == "Pass":
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
    def get_valid_gamemodes(player):
        valid_gamesmodes = [
            {"name": "Null", "active_player": player},
            {"name": "Kreuz", "active_player": player},
            {"name": "Pik", "active_player": player},
            {"name": "Herz", "active_player": player},
            {"name": "Karo", "active_player": player},
            {"name": "Grand", "active_player": player},
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
