from flask import request

from betmedium import BetMedium
from beteasy import BetEasy
from helpersbetting import HelpersBetting

class MakeAIGamemodeBet:
    @staticmethod
    def make_ai_gamemode_bet(data):
        make_ai_gamemode_bet = data
        ai_model = make_ai_gamemode_bet.get("ai_model")
        hand = make_ai_gamemode_bet.get("hand")
        previous_bets = make_ai_gamemode_bet.get("previous_bets")
        player_order = make_ai_gamemode_bet.get("players")

        # Sicherstellen, dass 'previous_bets' nicht leer ist
        if not previous_bets:
            return {"name": "Raise", "active_player": player_order[2], "betting": 18}

        # Den letzten Spieler aus den vorherigen Wetten extrahieren
        player = previous_bets[-1].get("gamemode").get("active_player")

        if ai_model == "easy":
            # Sicherstellen, dass betting_ai_easy ein gültiges Ergebnis zurückgibt
            result = BetEasy.betting_ai_easy(hand, previous_bets, player)
            return MakeAIGamemodeBet.get_next_bid(result, player, previous_bets)
        
        elif ai_model == "medium":
            # Sicherstellen, dass betting_ai_medium ein gültiges Ergebnis zurückgibt
            result = BetMedium.betting_ai_medium(hand, previous_bets, player)
            return MakeAIGamemodeBet.get_next_bid(result, player, previous_bets)

    @staticmethod
    def get_next_bid(result, player, previous_bets):
        # Sicherstellen, dass result genug Einträge hat
        if len(result) < 2:
            raise ValueError("Nicht genug Ergebnisse in 'result' vorhanden")

        skat_bid_table = HelpersBetting.create_skat_bid_table(player)

        # Überprüfen, ob der letzte Einsatz gleich dem vorletzten Einsatz ist
        if int(result[-1].get("gamemode").get("betting")) == int(result[-2].get("gamemode").get("betting")):
            return {"name": "Pass", "active_player": player, "betting": previous_bets[-1].get("betting")}
        else:
            # Das nächsthöhere Gebot aus der skat_bid_table finden
            y = next(y for y in skat_bid_table if (int(y.get("gamemode").get("betting")) > int(result[-2].get("gamemode").get("betting")), None))
            if not y:
                raise ValueError("Kein höheres Gebot in skat_bid_table gefunden")

            # Wenn der letzte Einsatz "Check" oder "Pass" war, dann "Raise"
            if previous_bets[-1].get("gamemode").get("name") == "Check" or previous_bets[-1].get("gamemode").get("name") == "Pass":
                return {"name": "Raise", "active_player": player, "betting": y.get("betting")}
            else:
                return {"name": "Check", "active_player": player, "betting": previous_bets[-1].get("betting")}
