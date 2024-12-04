import random
from calculatebids import CalculateBids

class BetEasy:
    @staticmethod
    def betting_ai_easy(hand,previous_bets,player):
        valid_bets = CalculateBids.calculate_bids(hand, player)
        valid_bets.sort(key = lambda bet: int(bet['betting']))
        last_bid = previous_bets[-1]

        result = [last_bid]

        ran = random.randint(1,10)
        if ran >=7:
            for x in valid_bets:
                if int(x.get("betting")) > int(last_bid.get("betting")):
                    result.append(x)
                    return result
        else:
            result.append(last_bid)
            return result