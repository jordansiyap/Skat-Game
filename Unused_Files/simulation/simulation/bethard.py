from beteasy import BetEasy
from betmedium import BetMedium
from calculatebids import CalculateBids
from bethard_prediction import BetHardPrediction
from helpersbetting import HelpersBetting


class BetHard:

    @staticmethod
    def betting_ai_hard(hand, previous_bets,player):
        valid_bids = CalculateBids.calculate_bids(hand, player)
        last_bid = BetEasy.find_last_bid(previous_bets, player).get("gamemode")
        for bid in valid_bids[:]:
            if int(bid.get("betting")) < int(last_bid.get("betting")):
                valid_bids.remove(bid)


        priority_last_bid = BetHard.calculate_heighest_priority_of_last_bid(hand, player, last_bid["betting"])

        weighted_valid_bets = []
        for gamemode in valid_bids:
            weighted_valid_bets.append(BetHard.calculate_weight(hand, gamemode))
        weighted_valid_bets.sort(key=lambda bet: int(bet['betting']))
        result = [last_bid]
        for x in weighted_valid_bets:
            if float(x.get("priority")) >= float(priority_last_bid.get("priority")) and int(x.get("betting")) > int(
                    priority_last_bid.get("betting")):
                result.append(x)
                return result
        result.append(last_bid)
        return result

    @staticmethod
    def calculate_weight(hand, gamemode):
        weight = 0
        predictor = BetHardPrediction(hand,gamemode)
        if gamemode.get("name") != "Null":
            if gamemode.get("name") == "Kreuz":
                weight += BetHard.count_weights(predictor.hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Pik":
                weight += BetHard.count_weights(predictor.hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Herz":
                weight += BetHard.count_weights(predictor.hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Karo":
                weight += BetHard.count_weights(predictor.hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Grand":
                weight += BetHard.count_weights(predictor.hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
        else:
            weight += BetMedium.count_lowies(predictor.hand) * 50
        weight += int(gamemode.get("betting"))
        return {"name": gamemode.get("name"), "active_player": gamemode.get("active_player"),
                "description": gamemode.get("description"),
                "betting": gamemode.get("betting"), "priority": str(weight)}

    @staticmethod
    def count_weights(hand):
        count = 0
        for card in hand:
            count += float(card["win"])
        return count

    @staticmethod
    def calculate_heighest_priority_of_last_bid(hand, player, betting):
        skat_bid_table = []
        if int(betting) == 23:
            skat_bid_table.append(BetHard.calculate_weight(hand, {"name": "Null", "active_player": player,
                                                                    "description": "Nullspiel", "betting": "23"}))
        if int(betting) == 35:
            skat_bid_table.append(BetHard.calculate_weight(hand, {"name": "Null", "active_player": player,
                                                                    "description": "Nullspiel Hand", "betting": "35"}))

        modes = ["Karo", "Herz", "Pik", "Kreuz", "Grand"]

        for mode in modes:
            for x in range(1, 6):
                bid = HelpersBetting.create_gamemode(mode, player, x)
                if int(bid["betting"]) == int(betting):
                    skat_bid_table.append(BetHard.calculate_weight(hand, bid))
        skat_bid_table.sort(key=lambda bet: float(bet['priority']))
        return skat_bid_table[-1]
