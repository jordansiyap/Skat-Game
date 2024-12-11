from calculatebids import CalculateBids

class BetMedium:
    @staticmethod
    def betting_ai_medium(hand,previous_bets,player):
        valid_bids = CalculateBids.calculate_bids(hand, player)
        last_bid = BetMedium.calculate_weight(hand, previous_bets[-1])

        weighted_valid_bets = []
        for gamemode in valid_bids:
            weighted_valid_bets.append(BetMedium.calculate_weight(hand, gamemode))
        weighted_valid_bets.sort(key=lambda bet: int(bet['betting']))
        result = [last_bid]
        for x in weighted_valid_bets:
            if int(x.get("priority")) > int(last_bid.get("priority")) and int(x.get("betting")) > int(last_bid.get("betting")):
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
                weight += BetMedium.count_spaes(hand) * 20
                if "Hand" in gamemode.get("description"):
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
    def count_spaes(hand):
        counter = 0
        for card in hand:
            if card.get("suit") == "spaes" and card.get("value") != "jack":
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
