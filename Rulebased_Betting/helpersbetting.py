"""
Hilfsklasse
Implementiert Methoden zur Erstellung von Spielmodi
"""
class HelpersBetting:

    @staticmethod
    def create_skat_bid_table(player):
        skat_bid_table = [
            {"name": "Null", "active_player": player, "description": "Nullspiel", "betting": "23"},
            {"name": "Null", "active_player": player, "description": "Nullspiel Hand", "betting": "35"},
        ]

        modes = ["Karo", "Herz", "Pik", "Kreuz", "Grand"]

        for mode in modes:
            for x in range(1, 6):
                bid = HelpersBetting.create_gamemode(mode, player, x)
                y = next((y for y in skat_bid_table if int(y["betting"]) == int(bid["betting"])), None)
                if y is None:
                    skat_bid_table.append(bid)
        skat_bid_table.sort(key=lambda bet: int(bet['betting']))
        return skat_bid_table

    @staticmethod
    def create_gamemode(mode, player, number):
        if mode == "Karo":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 9)}
        elif mode == "Herz":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 10)}
        elif mode == "Pik":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 11)}
        elif mode == "Kreuz":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 12)}
        elif mode == "Grand":
            return {"name": mode, "active_player": player,
                    "betting": str((number + 1) * 24)}