from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.beteasy import BetEasy
from Rulebased_Betting.helpersbetting import HelpersBetting

class BetMedium:
    @staticmethod
    def betting_ai_medium(hand,previous_bets,player):
        valid_bids = CalculateBids.calculate_bids(hand, player)
        last_bid = BetEasy.find_last_bid(previous_bets,player).get("gamemode")
        for bid in valid_bids[:]:
            if int(bid.get("betting")) < int(last_bid.get("betting")):
                valid_bids.remove(bid)

        priority_last_bid = BetMedium.calculate_heighest_priority_of_last_bid(hand,player,last_bid["betting"])

        weighted_valid_bets = []
        for gamemode in valid_bids:
            weighted_valid_bets.append(BetMedium.calculate_weight(hand, gamemode))
        weighted_valid_bets.sort(key=lambda bet: int(bet.get('betting')))
        result = [last_bid]
        for x in weighted_valid_bets:
            if int(x.get("priority")) >= int(priority_last_bid.get("priority")) and int(x.get("betting")) > int(priority_last_bid.get("betting")):
                result.append(x)
                return result
        result.append(last_bid)
        return result

    @staticmethod
    def calculate_weight(hand,gamemode):
        weight=0
        if gamemode.get("name") != "Null":
            weight += BetMedium.count_jacks(hand) * 100
            if gamemode.get("name") == "Kreuz":
                weight += BetMedium.count_clubs(hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Pik":
                weight += BetMedium.count_spades(hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Herz":
                weight += BetMedium.count_hearts(hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Karo":
                weight += BetMedium.count_diamonds(hand) * 20
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
            elif gamemode.get("name") == "Grand":
                weight += BetMedium.count_jacks(hand) * 25
                if "Hand" in str(gamemode.get("description")):
                    weight -= 30
        else:
            weight += BetMedium.count_lowies(hand) * 50
        weight += int(gamemode.get("betting"))
        return {"name": gamemode.get("name"), "active_player": gamemode.get("active_player"),
                            "description": gamemode.get("description"),
                            "betting": gamemode.get("betting"), "priority": str(weight) }

    @staticmethod
    def count_jacks(hand):
        counter = 0
        for card in hand:
            if card.get("value") == "jack":
                counter +=1
        return counter

    @staticmethod
    def count_clubs(hand):
        counter = 0
        for card in hand:
            if card.get("suit") == "clubs" and card.get("value") != "jack":
                counter +=1
        return counter

    @staticmethod
    def count_spades(hand):
        counter = 0
        for card in hand:
            if card.get("suit") == "spades" and card.get("value") != "jack":
                counter +=1
        return counter

    @staticmethod
    def count_hearts(hand):
        counter = 0
        for card in hand:
            if card.get("suit") == "hearts" and card.get("value") != "jack":
                counter +=1
        return counter

    @staticmethod
    def count_diamonds(hand):
        counter = 0
        for card in hand:
            if card.get("suit") == "diamonds" and card.get("value") != "jack":
                counter +=1
        return counter

    @staticmethod
    def count_lowies(hand):
        counter = 0
        for card in hand:
            if card.get("value") != "jack" and card.get("value") != "ace" and card.get("value") != "king" and card.get("value") != "queen":
                counter += 1
        return counter

    @staticmethod
    def calculate_heighest_priority_of_last_bid(hand,player,betting):
        skat_bid_table = []
        if int(betting) == 23:
            skat_bid_table.append(BetMedium.calculate_weight(hand,{"name": "Null", "active_player": player, "description": "Nullspiel", "betting": "23"}))
        if int(betting) == 35:
            skat_bid_table.append(BetMedium.calculate_weight(hand,{"name": "Null", "active_player": player, "description": "Nullspiel Hand", "betting": "35"}))

        modes = ["Karo", "Herz", "Pik", "Kreuz", "Grand"]

        for mode in modes:
            for x in range(1, 6):
                bid = HelpersBetting.create_gamemode(mode, player, x)
                if int(bid.get("betting")) == int(betting):
                    skat_bid_table.append(BetMedium.calculate_weight(hand,bid))
        skat_bid_table.sort(key=lambda bet: int(bet.get('priority')))
        return skat_bid_table[-1]