import random
from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.helpersbetting import HelpersBetting

"""Regelbasiertes Reizen einfach"""
class BetEasy:
    """Zufallsbasiert"""
    @staticmethod
    def betting_ai_easy(hand,previous_bets,player):
        valid_bids = CalculateBids.calculate_bids(hand, player)
        last_bid = BetEasy.find_last_bid(previous_bets,player).get("gamemode")

        result = [last_bid]


        ran = random.randint(1,10)
        if ran >=7:
            for x in valid_bids:
                if int(x.get("betting")) > int(last_bid.get("betting")):
                    result.append(x)
                    return result
        else:
            result.append(last_bid)
            return result

    """Findet das letzte Erhöhen"""
    @staticmethod
    def find_last_bid(previous_bets, player):
        skat_bid_table = HelpersBetting.create_skat_bid_table(player)
        skat_bid_table.sort(reverse=True, key=lambda bet: int(bet['betting']))
        if previous_bets[-1].get("gamemode").get("name") == "Raise:":
            y = next((y for y in skat_bid_table if int(y.get("gamemode")["betting"]) < int(previous_bets[-1].get("gamemode")["betting"])), None)
            return y
        else:
            return previous_bets[-1]